#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
from src.fmods import FMods
from src.docker import Docker
from src.postgre import Postgre

class TestPostgre(unittest.TestCase):

  def testFModsPostgre(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('pg'), {})
    self.assertEqual(fm.getTmpFolder('pg'), 'data/tmp/git/pg')

    fm.scan()
    self.assertEqual(fm.count(), 7)

    config_need = dict(sorted({('CONTAINER_ENV_POSTGRES_DB', 'test-db'), ('CONTAINER_ENV_POSTGRES_PASSWORD', 'pwd'), ('CONTAINER_ENV_POSTGRES_USER', 'user'), ('CONTAINER_NAME', 'pg-test'), ('DB_PORT', '17432'), ('CONTAINER_PORTS', '17432:5432'), ('CONTAINER_NAME', 'pg-test'), ('CONTAINER_SRC', 'postgres:alpine'), ('DB_NAME', 'test-db'), ('DB_PASSWORD', 'pwd'), ('DB_USER', 'user'), ('NAME', 'pg'), ('TYPE', 'docker')}))
    cfg = fm.getConfig('pg')
    cfg.pop('MOD_PATH', None)
    self.assertEqual(cfg, config_need)
    
    pg = Postgre(fm.getConfig('pg'), fm.getTmpFolder('pg'), True)
    
    dbconn = pg.getConnect('pg')
    self.assertIsNone(dbconn)

    # Start service
    srvPg = Docker(fm.getConfig('pg'), fm.getTmpFolder('pg'), True)

    ok = srvPg.run()
    self.assertTrue(ok)
    res = srvPg.status()
    self.assertEqual(res, 'running')

    time.sleep(2)

    # Test connect
    dbconn = pg.getConnect('pg')
    self.assertIsNotNone(dbconn)
    tbl = pg.getTableList()
    self.assertEqual(tbl, [])
    
    self.assertTrue(pg.loadSQL('data/postgre/create_table.sql'))
    
    tbl = pg.getTableList()
    self.assertEqual(tbl, [('public', 'article')])

    self.assertTrue(pg.loadSQL('data/postgre/create_tables.sql'))
    
    tbl = pg.getTableList()
    self.assertEqual(tbl, [('public', 'article'), ('public', 'article2'), ('public', 'article3')])
    
    res = pg.getData('select * from public.article')
    self.assertEqual(res, [])
    
    self.assertTrue(pg.loadSQL('data/postgre/insert.sql'))
    res = pg.getData('select * from public.article')
    self.assertEqual(res, [(1, 'article 1', 'description', None)])

    # Remove
    ok = srvPg.remove()
    self.assertEqual(ok, True)
    
    res = srvPg.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()
