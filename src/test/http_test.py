#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
import os
from src.fmods import FMods

class TestHTTP(unittest.TestCase):

  def testFModsHTTP(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)

    fm.scan()
    self.assertTrue(fm.count() > 1)

    # Start service
    srvHTTP = fm.newHTTPServer('http')

    self.assertEqual(srvHTTP.status(), 'stopped')
    self.assertTrue(srvHTTP.start())
    self.assertEqual(srvHTTP.status(), 'running')

    http = fm.newHTTP('http')
    
    res, ok = http.getStatusLiveness()
    self.assertEqual(res, 'ok')
    self.assertTrue(ok)
    
    # Remove
    self.assertTrue(srvHTTP.stop())
    self.assertEqual(srvHTTP.status(), 'stopped')


if __name__ == '__main__':
  unittest.main()
