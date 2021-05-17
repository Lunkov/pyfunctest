#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import git
import shutil
import docker
import traceback
import pika
import filecmp
from pprint import pprint

class RabbitMQ():
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
    self.verbose = verbose
    self.config = config
    self.pathTmp = pathTmp
    self.moduleName = self.config['NAME']
    self.connect = None
    self.channel = None
  
  def getConnect(self):
    """ Connect to rabbitMQ
    """
    self.url = 'amqp://localhost'
    if 'RABBITMQ_URL' in self.config:
      self.url = self.config['RABBITMQ_URL']
      
    self.channel = 1
    if 'RABBITMQ_CHANNEL' in self.config:
      self.channel = int(self.config['RABBITMQ_CHANNEL'])

    self.rmq_parameters = pika.URLParameters(self.url)
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
        self.channel = self.connect.channel(self.channel)
      except Exception as e:
        print("DBG: WAIT: %d: Connect to channel of RabbitMQ '%s':%s" % (elapsed_time, self.url, str_err))
        str_err = str(e)

    if self.channel is None:
      print("FATAL: Connect to channel of RabbitMQ '%s': %s" % (self.url, str_err))
      return None
    
    self.channel.confirm_delivery()
    return self.channel

  def close(self):
    #try:
    #  if not self.channel is None:
    #    self.channel.close()
    #except Exception as e:
    #  print("ERR: Close channel of RabbitMQ '%s': %s" % (self.url, str(e)))
    try:
      if not self.connect is None:
        self.connect.close()
    except Exception as e:
      print("ERR: Close connect to RabbitMQ '%s': %s" % (self.url, str(e)))
    self.connect = None
    self.channel = None
    
  def send(self, queue, exchange, key, message):
    #if self.reconnect() is None:
    #  print("FATAL: Send to closed RabbitMQ '%s'" % (self.url))
    #  return False
    try:
      self.channel.queue_declare(queue = queue)
      self.channel.exchange_declare(exchange)
      #self.channel.tx_select()
      self.channel.basic_publish(exchange = exchange, routing_key = key, body = message)
      #self.channel.tx_commit()
      #self.close()
      if self.verbose:
        print("DBG: Sended message to RabbitMQ '%s': queue = '%s'" % (self.url, queue))
    except Exception as e:
      print("FATAL: Send to RabbitMQ '%s': %s" % (self.url, str(e)))
      return False
      
    return True

  def sendFile(self, queue, exchange, key, fileName):
    #if self.reconnect() is None:
    #  print("FATAL: Send to closed RabbitMQ '%s'" % (self.url))
    #  return False
    try:
      msgFile = open(fileName,'r')
      self.channel.queue_declare(queue = queue)
      self.channel.exchange_declare(exchange)
      self.channel.basic_publish(exchange = exchange, routing_key = key, body = msgFile.read())
      if self.verbose:
        print("DBG: Send message to RabbitMQ '%s': queue = '%s'" % (self.url, queue))
    except Exception as e:
      print("FATAL: Sended to RabbitMQ '%s': %s" % (self.url, str(e)))
      return False
      
    return True

  def receive(self, queue, key):
    message = ''
    try:
      # self.channel.queue_declare(queue = queue)
      method_frame, header_frame, message = self.channel.basic_get(queue = queue)
      if self.verbose:
        print("DBG: Receive from RabbitMQ '%s': '%s', header='%s', msg='%s'" % (self.url, method_frame, header_frame, message))
      pprint(header_frame)
      pprint(message)
      pprint(method_frame)
      if method_frame:
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return message, True
      else:            
        print("LOG: Has not messages from RabbitMQ '%s'" % (self.url))
        return '', False
    except Exception as e:
      print("FATAL: Recieve from RabbitMQ '%s': %s" % (self.url, str(e)))
      return '', False
      
    return message, True

