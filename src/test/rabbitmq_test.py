#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import requests
import time
from src.fmods import FMods

class TestRabbitMQ(unittest.TestCase):

  def testFModsRabbitMQ(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('rabbitmq'), {})
    self.assertEqual(fm.getTmpFolder('rabbitmq'), 'data/tmp/git/rabbitmq')

    fm.scan()
    self.assertTrue(fm.count() > 7)

    rabbitmq1 = fm.newRabbitMQ('rabbitmq')
    
    #conn = rabbitmq1.getConnect()
    #self.assertIsNone(conn)

    # Start service
    #srvRabbitMQ = fm.newDocker('rabbitmq')

    #self.assertTrue(srvRabbitMQ.run())
    #self.assertEqual(srvRabbitMQ.status(), 'running')

    time.sleep(5)

    # Test connect
    conn = rabbitmq1.getConnect()
    self.assertIsNotNone(conn)
    
    channel = 'channel-test'
    exchange = 'exchange-test'
    key = 'key-test'

    self.assertTrue(rabbitmq1.send(channel, exchange, key, 'message 1'))
    self.assertTrue(rabbitmq1.send(channel, exchange, key, 'message 2'))
    self.assertTrue(rabbitmq1.send(channel, exchange, key, 'message 3'))
    self.assertTrue(rabbitmq1.send(channel, exchange, key, 'message 4'))
    self.assertTrue(rabbitmq1.send(channel, exchange, key, 'message 5'))

    rabbitmq2 = fm.newRabbitMQ('rabbitmq')
    conn = rabbitmq2.getConnect()
    self.assertIsNotNone(conn)
    
    time.sleep(25)
    
    msg, ok = rabbitmq2.receive(channel, key)
    self.assertTrue(ok)
    self.assertEqual(msg, 'message')

    rabbitmq1.close()
    rabbitmq2.close()
    # Remove
    #self.assertTrue(srvRabbitMQ.remove())
    #self.assertEqual(srvRabbitMQ.status(), 'not found')


if __name__ == '__main__':
  unittest.main()
