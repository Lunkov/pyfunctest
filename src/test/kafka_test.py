#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import requests
import time
from src.fmods import FMods

class TestKafka(unittest.TestCase):

  def testFModsKafka(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('kafka'), {})
    self.assertEqual(fm.getTmpFolder('kafka'), 'data/tmp/git/kafka')

    fm.scan()
    self.assertTrue(fm.count() > 7)

    channel = 'channel-test'
    
    kafka1 = fm.newKafka('kafka')
    kafka2 = fm.newKafka('kafka')

    # Start service
    srvKafka = fm.newDocker('kafka')

    self.assertTrue(srvKafka.startCompose(os.path.join(os.getcwd(), 'data/mods/kafka/docker-compose.yml')))
    self.assertTrue(srvKafka.statusWaiting('running'))
    self.assertEqual(srvKafka.status(), 'running')

    # Test connect
    self.assertIsNotNone(kafka1.reconnect())
    
    self.assertTrue(kafka1.send(channel, 'message 1'))

    msg, ok = kafka2.receive(channel)
    self.assertTrue(ok)
    self.assertEqual(msg, 'message 1')
    
    # kafka2.receiveAll(channel)
    
    self.assertTrue(kafka1.sendFile(channel, 'data/files/test.txt'))
    self.assertTrue(kafka2.receiveAndCompareFile(channel, 'data/files/test.txt'))

    kafka1.close()
    kafka2.close()

    # Remove
    self.assertTrue(srvKafka.stopCompose(os.path.join(os.getcwd(), 'data/mods/kafka/docker-compose.yml')))
    self.assertEqual(srvKafka.status(), 'not found')


if __name__ == '__main__':
  unittest.main()
