#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import requests
import time
import pika
from src.fmods import FMods

class TestRabbitMQ(unittest.TestCase):

  def testFModsRabbitMQ(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('rabbitmq'), {})
    self.assertEqual(fm.getTmpFolder('rabbitmq'), 'data/tmp/git/rabbitmq')

    fm.scan()
    self.assertTrue(fm.count() > 1)

    rabbitmq1 = fm.newRabbitMQ('rabbitmq')
    
    #conn = rabbitmq1.getConnect()
    #self.assertIsNone(conn)

    # Start service
    srvRabbitMQ = fm.newDocker('rabbitmq')

    self.assertTrue(srvRabbitMQ.run())
    self.assertTrue(srvRabbitMQ.statusWaiting('running'))
    self.assertEqual(srvRabbitMQ.status(), 'running')

    # Test connect
    queue = 'log3'
    exchange = 'log3'
    routing_key = ''
    exchange_type = 'fanout'
    
    rabbitmq1.init()
    #self.assertTrue(rabbitmq1.createRoute(exchange, exchange_type, routing_key, queue))
    
    self.assertTrue(rabbitmq1.send(exchange, routing_key, 'message 1'))
    self.assertTrue(rabbitmq1.send(exchange, routing_key, 'message 2'))

    rabbitmq2 = fm.newRabbitMQ('rabbitmq')
    
    time.sleep(1)
    
    msg, ok = rabbitmq2.receive(queue)
    self.assertTrue(ok)
    self.assertEqual(msg, 'message 1')

    msg, ok = rabbitmq2.receive(queue)
    self.assertTrue(ok)
    self.assertEqual(msg, 'message 2')


    self.assertTrue(rabbitmq1.sendFile(exchange, routing_key, 'data/files/test.txt'))
    self.assertTrue(rabbitmq1.receiveAndCompareFile(queue, 'data/files/test.txt'))

    rabbitmq1.close()
    rabbitmq2.close()

    # Remove
    self.assertTrue(srvRabbitMQ.remove())
    self.assertEqual(srvRabbitMQ.status(), 'not found')


if __name__ == '__main__':
  unittest.main()
