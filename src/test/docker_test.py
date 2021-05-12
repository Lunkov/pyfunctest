#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
from src.fmods import FMods
from src.docker import Docker
from src.git import GIT

class TestDocker(unittest.TestCase):

  def testDockerRun000(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 7)

    srvNginx000 = Docker(fm.getConfig('nginx-000'), fm.getTmpFolder('nginx-000'), True)

    # 
    res, ok = srvNginx000.logs()
    self.assertEqual(ok, False)

    res = srvNginx000.status()
    self.assertEqual(res, 'not found')


  def testDockerRun(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 5)

    srvNginx = Docker(fm.getConfig('nginx'), fm.getTmpFolder('nginx'), True)

    srvNginx.stop()
    srvNginx.remove()
    
    res = srvNginx.status()
    self.assertEqual(res, 'not found')
    
    res, ok = srvNginx.logs()
    self.assertEqual(ok, False)
    self.assertEqual(res, '')

    # Test: Docker run
    ok = srvNginx.run()
    self.assertEqual(ok, True)
    res = srvNginx.status()
    self.assertEqual(res, 'running')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertEqual(r.status_code, 404)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

    res = srvNginx.status()
    self.assertEqual(res, 'running')

    ok = srvNginx.remove()
    self.assertEqual(ok, True)
    
    res = srvNginx.status()
    self.assertEqual(res, 'not found')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertEqual(r.status_code, None)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

  def testDockerBuild(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 5)
   
    # Test: Docker build
    srvGit = GIT(fm.getConfig('srv-report'), fm.getTmpFolder('srv-report'), True)
    srvDocker = Docker(fm.getConfig('srv-report'), fm.getTmpFolder('srv-report'), True)
    
    ok = srvGit.clone()
    self.assertEqual(ok, True)
    
    self.assertEqual(True, srvDocker.statusWaiting('not found'))
    
    ok = srvDocker.build()
    self.assertEqual(ok, True)

    ok = srvDocker.run()
    self.assertEqual(ok, True)
    
    res = srvDocker.status()
    self.assertEqual(res, 'running')

    self.assertEqual(True, srvDocker.statusWaiting('running'))
    
    ok = srvDocker.remove()
    self.assertEqual(ok, True)
    
    res = srvDocker.status()
    self.assertEqual(res, 'not found')

if __name__ == '__main__':
  unittest.main()
