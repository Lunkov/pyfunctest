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

    kafka = fm.newKafka('kafka')

    # Start service
    srvKafka = fm.newDocker('kafka')

    self.assertTrue(srvKafka.startCompose(os.path.join(os.getcwd(), 'data/mods/kafka/docker-compose.yml')))
    self.assertTrue(srvKafka.statusWaiting('running'))
    self.assertEqual(srvKafka.status(), 'running')

    time.sleep(2)

    # Test connect
    #conn = kafka.getConnect()
    #self.assertIsNotNone(conn)

    self.assertTrue(kafka.send('channel-test', 'message 1'))

    msg, ok = kafka.receive('channel-test')
    self.assertTrue(ok)
    self.assertEqual(msg, 'message 1')
    
    # Remove
    self.assertTrue(srvKafka.stopCompose(os.path.join(os.getcwd(), 'data/mods/kafka/docker-compose.yml')))
    self.assertEqual(srvKafka.status(), 'not found')


if __name__ == '__main__':
  unittest.main()
