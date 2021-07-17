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
from kafka.admin  import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
from .fmod import FMod

class Kafka(FMod):
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
    super(Kafka, self).__init__(config, pathTmp, verbose)

    self.consumer = None
    self.producer = None
    self.url_in = 'localhost:9092'
    self.url_out = 'localhost:9094'
    self.id_group = 'test'
    if 'kafka' in self.config:
      if 'url_inside' in self.config['kafka']:
        self.url_in = self.config['kafka']['url_inside']

      if 'url_outside' in self.config['kafka']:
        self.url_out = self.config['kafka']['url_outside']

      if 'id_group' in self.config['kafka']:
        self.id_group = self.config['kafka']['id_group']
  
  def getConnect(self):
    """ Connect to rabbitMQ
    """
    return self.reconnect()
    
  def reconnect(self):
    if self.consumer:
      return self.consumer
    self.close()

    if self.verbose:
      print("DBG: Reconnecting Kafka '%s'" % (self.url_in))

    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while (self.producer is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.producer = KafkaProducer(bootstrap_servers=self.url_out) # group_id=self.id_group
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
        self.consumer = KafkaConsumer(bootstrap_servers=self.url_out, enable_auto_commit=True, group_id=self.id_group, auto_commit_interval_ms=50, request_timeout_ms=11000, consumer_timeout_ms=2000, auto_offset_reset='latest')
      except Exception as e:
        str_err = str(e)
        print("DBG: WAIT: %d: Connect KafkaConsumer '%s':%s" % (elapsed_time, self.url_out, str_err))

    if self.consumer is None:
      print("FATAL: KafkaConsumer '%s': %s" % (self.url_out, str_err))
      return None

    if self.verbose:
      print("DBG: Reconnected Kafka '%s'" % (self.url_in))

    return self.consumer

  def close(self):
    if self.verbose:
      print("DBG: Close Kafka '%s'" % (self.url_in))
    if self.producer:
      self.producer.close()
    if self.consumer:
      self.consumer.close()
    self.consumer = None
    self.producer = None
    if self.verbose:
      print("DBG: Closed Kafka '%s'" % (self.url_in))

  def init(self):
    if not 'INIT_KAFKA_CREATE_CHANNELS' in self.config:
      return
    if self.reconnect() is None:
      return
    admin_client = KafkaAdminClient(bootstrap_servers=self.url_out) # group_id=self.id_group
    channels = self.config['INIT_KAFKA_CREATE_CHANNELS']
    achs = channels.split(';')
    topic_list = []
    for channel in achs:
      if self.verbose:
        print("DBG: createTopic in Kafka '%s': topic='%s'" % (self.url_out, channel))
      topic_list.append(NewTopic(name=channel, num_partitions=1, replication_factor=1))
    res = None
    try:
      res = admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as e:
      print("ERR: createTopic in Kafka '%s': err='%s'" % (self.url_out, str(e)))

    admin_client.close()
    
  def send(self, topic, message):
    self.reconnect()
    try:
      if self.verbose:
        print("DBG: Sending to Kafka '%s': topic='%s', msg='%s'" % (self.url_in, topic, message.encode('ascii')))
      self.producer.send(topic, message.encode('ascii'))
      self.producer.flush()
      if self.verbose:
        print("DBG: Send to Kafka '%s': topic='%s', msg='%s'" % (self.url_in, topic, message.encode('ascii')))
    except Exception as e:
      print("FATAL: Send to Kafka '%s': %s" % (self.url_in, str(e)))
      return False

    return True

  def sendFile(self, topic, fileName):
    try:
      msgFile = open(fileName,'r')
      self.reconnect()
      if self.verbose:
        print("DBG: Sending to Kafka '%s': topic='%s', fileName='%s'" % (self.url_in, topic, fileName))
      self.producer.send(topic, msgFile.read().encode('ascii'))
      self.producer.flush()
      if self.verbose:
        print("DBG: Send file to Kafka '%s': topic='%s', fileName='%s'" % (self.url_in, topic, fileName))
    except Exception as e:
      print("FATAL: Send to Kafka '%s': %s" % (self.url_in, str(e)))
      return False
      
    return True

  def receive(self, topic):
    self.reconnect()
    message = None
    try:
      if self.verbose:
        print("DBG: Recieving to Kafka '%s': topic='%s'" % (self.url_in, topic))
      partition = TopicPartition(topic, 0)
      self.consumer.assign([partition])
      self.consumer.seek_to_beginning(partition)
      # Read the message
      for message in self.consumer:
        continue
      if self.verbose:
        print("DBG: Receive from Kafka '%s': topic='%s', msg='%s'" % (self.url_in, topic, message.value))
    except Exception as e:
      print("FATAL: Recieve from Kafka '%s': %s" % (self.url_in, str(e)))
      return '', False
    
    return message.value.decode('ascii'), True


  def receiveAll(self, topic):
    self.reconnect()
    message = None
    try:
      if self.verbose:
        print("DBG: Recieving to Kafka '%s': topic='%s'" % (self.url_in, topic))
      partition = TopicPartition(topic, 0)
      self.consumer.assign([partition])
      self.consumer.seek_to_beginning(partition)
      # Read the message
      for message in self.consumer:
        if self.verbose:
          print("DBG: Receive from Kafka '%s': topic='%s', msg='%s'" % (self.url_in, topic, message.value))
    except Exception as e:
      print("FATAL: Recieve from Kafka '%s': %s" % (self.url_in, str(e)))
      return '', False
    
    return message.value.decode('ascii'), True

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
      print("FATAL: compareFiles Kafka(%s): %s" % (self.url, str(e)))
      return False
    return result
