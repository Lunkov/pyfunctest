#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
from src.fmods import FMods

class TestDocker(unittest.TestCase):

  def testDockerRun000(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertTrue(fm.count() > 7)

    srvNginx000 = fm.newDocker('nginx-000')

    # 
    res, ok = srvNginx000.logs()
    self.assertEqual(ok, False)

    res = srvNginx000.status()
    self.assertEqual(res, 'not found')


  def testDockerRun(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertTrue(fm.count() > 5)

    srvNginx = fm.newDocker('nginx')

    srvNginx.stop()
    srvNginx.remove()
    
    res = srvNginx.status()
    self.assertEqual(res, 'not found')
    
    res, ok = srvNginx.logs()
    self.assertFalse(ok)
    self.assertEqual(res, '')

    # Test: Docker run
    self.assertTrue(srvNginx.run())
    self.assertEqual(srvNginx.status(), 'running')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertEqual(r.status_code, 404)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

    self.assertEqual(srvNginx.status(), 'running')
    self.assertTrue(srvNginx.remove())
    self.assertEqual(srvNginx.status(), 'not found')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertIsNone(r.status_code)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

  def testDockerBuild(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertTrue(fm.count() > 5)
   
    # Test: Docker build
    srvGit = fm.newGIT('srv-report')
    srvDocker = fm.newDocker('srv-report')
    
    self.assertTrue(srvGit.clone())
    self.assertTrue(srvDocker.statusWaiting('not found'))
    self.assertTrue(srvDocker.build())
    self.assertTrue(srvDocker.run())
    
    res = srvDocker.status()
    self.assertEqual(res, 'running')
    self.assertTrue(srvDocker.statusWaiting('running'))
    self.assertTrue(srvDocker.remove())
    self.assertEqual(srvDocker.status(), 'not found')

  def testDockerBigRun(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertTrue(fm.count() > 5)
    fm.startAll()
    
    fm.stopAll()
    
if __name__ == '__main__':
  unittest.main()
