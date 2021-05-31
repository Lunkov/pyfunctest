#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import filecmp
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from kafka.errors import KafkaError

class Kafka():
  ''' Class for work with Kafka '''

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
    self.consumer = None
    self.producer = None
    self.url_in = 'localhost:9092'
    self.url_out = 'localhost:9094'
    if 'KAFKA_URL_INSIDE' in self.config:
      self.url_in = self.config['KAFKA_URL_INSIDE']

    if 'KAFKA_URL_OUTSIDE' in self.config:
      self.url_out = self.config['KAFKA_URL_OUTSIDE']
  
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
    while (self.producer is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.producer = KafkaProducer(bootstrap_servers=self.url_out)
      except Exception as e:
        str_err = str(e)
        print("DBG: WAIT: %d: Connect KafkaProducer '%s':%s" % (elapsed_time, self.url_in, str_err))

    if self.producer is None:
      print("FATAL: KafkaProducer '%s': %s" % (self.url_in, str_err))
      return None
    
    elapsed_time = 0
    str_err = ''

    while (self.consumer is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.consumer = KafkaConsumer(bootstrap_servers=self.url_out, group_id='main', enable_auto_commit=True)
      except Exception as e:
        str_err = str(e)
        print("DBG: WAIT: %d: Connect KafkaConsumer '%s':%s" % (elapsed_time, self.url_out, str_err))

    if self.consumer is None:
      print("FATAL: KafkaConsumer '%s': %s" % (self.url_out, str_err))
      return None

    return self.consumer


  def close(self):
    if not self.producer is None:
      self.producer.close()
    if not self.consumer is None:
      self.consumer.close()
    self.consumer = None
    self.producer = None
    
  def send(self, topic, message):
    self.reconnect()
    try:
      self.producer.send(topic, message.encode('ascii'))
      self.producer.flush()
    except Exception as e:
      print("FATAL: Send to Kafka '%s': %s" % (self.url_in, str(e)))
      return False

    self.close()
    return True

  def sendFile(self, topic, fileName):
    try:
      msgFile = open(fileName,'r')
      self.reconnect()
      self.producer.send(topic, msgFile.read().encode('ascii'))
      self.producer.flush()
      self.close()
    except Exception as e:
      print("FATAL: Send to Kafka '%s': %s" % (self.url_in, str(e)))
      return False
      
    return True

  def receive(self, topic):
    self.reconnect()
    message = None
    try:
      partition = TopicPartition(topic, 0)
      self.consumer.assign([partition])
      self.consumer.seek(partition, 0)
      # Read the message
      message = next(self.consumer)
      if self.verbose:
        print("DBG: Receive from Kafka '%s': topic='%s', msg='%s'" % (self.url_in, topic, message.value))
    except Exception as e:
      print("FATAL: Recieve from Kafka '%s': %s" % (self.url_in, str(e)))
      return '', False
    
    self.close()
    return message.value.decode('ascii'), True
