#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import pika
import filecmp
from .fmod import FMod

class RabbitMQ(FMod):
  ''' Class for work with RabbitMQ '''

  def __init__ (self, config, pathTmp, verbose):
    """ Initialising object
    Parameters
    ----------
    config : dict
        config of module
    pathTmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    super(RabbitMQ, self).__init__(config, pathTmp, verbose)

    self.connect = None
    self.channel = None
    self.url = 'amqp://localhost'
    if 'rabbitmq' in self.config:
      if 'url' in self.config['rabbitmq']:
        self.url = self.config['rabbitmq']['url']
    self.rmq_parameters = pika.URLParameters(self.url)
      
  def getConnect(self):
    """ Connect to rabbitMQ
    """
    return self.reconnect()
    
  def reconnect(self):
    self.close()
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while (self.connect is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.connect = pika.BlockingConnection(self.rmq_parameters)
      except Exception as e:
        print("DBG: WAIT: %d: Connect to RabbitMQ '%s':%s" % (elapsed_time, self.url, str_err))
        str_err = str(e)
        
    if self.connect is None:
      print("FATAL: Connect to RabbitMQ '%s': %s" % (self.url, str_err))
      return None

    elapsed_time = 0
    str_err = ''

    while (self.channel is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.channel = self.connect.channel()
      except Exception as e:
        print("DBG: WAIT: %d: Connect to channel of RabbitMQ '%s':%s" % (elapsed_time, self.url, str_err))
        str_err = str(e)

    if self.channel is None:
      print("FATAL: Connect to channel of RabbitMQ '%s': %s" % (self.url, str_err))
      return None
    
    self.channel.confirm_delivery()
    return self.channel

  def close(self):
    try:
      if not self.channel is None:
        self.channel.close()
    except Exception as e:
      print("ERR: Close channel of RabbitMQ '%s': %s" % (self.url, str(e)))
    try:
      if not self.connect is None:
        self.connect.close()
    except Exception as e:
      print("ERR: Close connect to RabbitMQ '%s': %s" % (self.url, str(e)))
    self.connect = None
    self.channel = None

  def init(self):
    if not 'rabbitmq' in self.config:
      return
    if not 'init' in self.config['rabbitmq']:
      return
    if not 'create_channels' in self.config['rabbitmq']['init']:
      return
    channels = self.config['rabbitmq']['init']['create_channels']
    for channel in channels:
      ch = channel.split(':')
      if len(ch) == 4:
        self.createRoute(ch[0], ch[1], ch[2], ch[3])

  def createRoute(self, exchange, exchange_type, key, queue):
    if self.reconnect() is None:
      print("FATAL: createRoute to closed RabbitMQ '%s'" % (self.url))
      return False
    try:
      self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
      self.channel.queue_declare(queue)
      self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)
      if self.verbose:
        print("DBG: createRoute in RabbitMQ '%s': exchange='%s' type='%s' routing_key='%s' queue='%s'" % (self.url, exchange, exchange_type, key, queue))
    except Exception as e:
      print("ERR: createRoute in RabbitMQ '%s': %s" % (self.url, str(e)))
      return False
    self.close()
    return True
    
  def send(self, exchange, key, message):
    if self.reconnect() is None:
      print("FATAL: Send to closed RabbitMQ '%s'" % (self.url))
      return False
    try:
      self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
      self.channel.basic_publish(exchange = exchange, routing_key = key, body = message)

      if self.verbose:
        print("DBG: Sended message to RabbitMQ '%s': exchange = '%s'" % (self.url, exchange))
    except Exception as e:
      print("FATAL: Send to RabbitMQ '%s': %s" % (self.url, str(e)))
      return False

    return True

  def sendFile(self, exchange, key, fileName):
    if self.reconnect() is None:
      print("FATAL: Send to closed RabbitMQ '%s'" % (self.url))
      return False
    try:
      msgFile = open(fileName,'r')
      self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
      self.channel.basic_publish(exchange = exchange, routing_key = key, body = msgFile.read())
      if self.verbose:
        print("DBG: Send message to RabbitMQ '%s': exchange = '%s'" % (self.url, exchange))
    except Exception as e:
      print("FATAL: Sended to RabbitMQ '%s': %s" % (self.url, str(e)))
      return False
      
    return True

  def receive(self, queue):
    if self.reconnect() is None:
      print("FATAL: Receive to closed RabbitMQ '%s'" % (self.url))
      return '', False
    message = ''
    try:
      
      method_frame, header_frame, message = self.channel.basic_get(queue = queue)
      if self.verbose:
        print("DBG: Receive from RabbitMQ '%s': '%s', header='%s', msg='%s'" % (self.url, method_frame, header_frame, message))
      if method_frame:
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return message.decode('ascii'), True
      else:            
        print("LOG: Has not messages from RabbitMQ '%s'" % (self.url))
        return '', False
    except Exception as e:
      print("FATAL: Recieve from RabbitMQ '%s': %s" % (self.url, str(e)))
      return '', False
      
    return message, True

  def receiveAndCompareFile(self, queue, fileName):
    msg, ok = self.receive(queue)
    if not ok:
      return False

    try:
      file1 = os.path.join(self.pathTmp, fileName)
      os.makedirs(os.path.dirname(file1), exist_ok=True)

      fileh = open(file1, 'w')
      fileh.write(msg)
      fileh.close()

      result = filecmp.cmp(file1, fileName, shallow=False)
      os.remove(file1)
    except Exception as e:
      print("FATAL: compareFiles RabbitMQ(%s): %s" % (self.url, str(e)))
      return False
    return result

