#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
from src.fmods import FMods

class TestFMods(unittest.TestCase):

  def testFModsSimple(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('pg'), {})
    self.assertEqual(fm.getTmpFolder('pg'), 'data/tmp/git/pg')
    
    fm.scan()
    self.assertEqual(fm.count(), 5)
    config_need = dict(sorted({('CONTAINER_NAME', 'pg-test'), ('CONTAINER_SRC', 'postgres:alpine'), ('DB_NAME', 'test-db'), ('DB_PASSWORD', 'pwd'), ('DB_USER', 'user'), ('NAME', 'pg'), ('TYPE', 'docker')}))
    cfg = fm.getConfig('pg')
    cfg.pop('MOD_PATH', None)
    self.assertEqual(cfg, config_need)
    
    dbconn = fm.getConnectToPostreSQL('pg')
    self.assertEqual(dbconn, None)

  def testFModsDockerRun(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 5)

    # Get Logs
    res, ok = fm.dockerLogs('nginx-000')
    self.assertEqual(ok, False)

    fm.dockerStop('nginx')
    fm.dockerRemove('nginx')
    
    res = fm.dockerStatus('nginx')
    self.assertEqual(res, 'not found')
    
    res, ok =fm.dockerLogs('nginx')
    self.assertEqual(ok, False)
    self.assertEqual(res, '')

    # Test: Docker run
    ok = fm.dockerRun('nginx')
    self.assertEqual(ok, True)
    res = fm.dockerStatus('nginx')
    self.assertEqual(res, 'running')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertEqual(r.status_code, 404)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

    res = fm.dockerStatus('nginx')
    self.assertEqual(res, 'running')

    ok = fm.dockerRemove('nginx')
    self.assertEqual(ok, True)
    
    res = fm.dockerStatus('nginx')
    self.assertEqual(res, 'not found')
    
    try:
      r = requests.get('http://127.0.0.1:3010')
      self.assertEqual(r.status_code, None)
    except Exception as e:
      print("FATAL: http://127.0.0.1:3010: %s" % (str(e)))

  def testFModsDockerBuild(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 5)
   
    # Test: Docker build
    ok = fm.gitClone('srv-report')
    self.assertEqual(ok, True)
    
    ok = fm.dockerBuild('srv-report')
    self.assertEqual(ok, True)
    
    ok = fm.dockerRun('srv-report')
    self.assertEqual(ok, True)
    
    res = fm.dockerStatus('srv-report')
    self.assertEqual(res, 'running')
    
    ok = fm.dockerRemove('srv-report')
    self.assertEqual(ok, True)
    
    res = fm.dockerStatus('srv-report')
    self.assertEqual(res, 'not found')

if __name__ == '__main__':
  unittest.main()
