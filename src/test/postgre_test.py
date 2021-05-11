#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
from src.fmods import FMods
from src.postgre import Postgre

class TestPostgre(unittest.TestCase):

  def testFModsPostgre(self):
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
    
    pg = Postgre(fm.getConfig('pg'), fm.getTmpFolder('pg'), True)
    
    dbconn = pg.getConnect('pg')
    self.assertEqual(dbconn, None)


if __name__ == '__main__':
  unittest.main()
