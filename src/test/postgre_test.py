#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
from src.fmods import FMods

class TestPostgre(unittest.TestCase):

  def testFModsPostgre(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('pg'), {})
    self.assertEqual(fm.getTmpFolder('pg'), 'data/tmp/git/pg')

    fm.scan()
    self.assertTrue(fm.count() > 7)

    #config_need = dict(sorted({('CONTAINER_ENV_POSTGRES_DB', 'test-db'), ('ORDER', 0), ('CONTAINER_ENV_POSTGRES_PASSWORD', 'pwd'), ('CONTAINER_ENV_POSTGRES_USER', 'user'), ('CONTAINER_NAME', 'pg-test'), ('DB_PORT', '17432'), ('CONTAINER_PORTS', '17432:5432'), ('CONTAINER_NAME', 'pg-test'), ('CONTAINER_SRC', 'postgres:alpine'), ('DB_NAME', 'test-db'), ('DB_PASSWORD', 'pwd'), ('DB_USER', 'user'), ('NAME', 'pg'), ('TYPE', 'docker')}))
    #cfg = fm.getConfig('pg')
    #cfg.pop('MOD_PATH', None)
    #self.assertEqual(cfg, config_need)
    
    pg = fm.newPostgre('pg')
    
    self.assertIsNone(pg.reconnect())

    # Start service
    srvPg = fm.newDocker('pg')

    ok = srvPg.run()
    self.assertTrue(ok)
    res = srvPg.status()
    self.assertEqual(res, 'running')

    # Test connect
    self.assertIsNotNone(pg.reconnect())
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

    # Migration
    mgPg = fm.newMigrate('pg')
    self.assertTrue(mgPg.run())
    self.assertEqual(pg.getTableList(), [('public', 'article'), ('public', 'article2'), ('public', 'article3'),('public', 'job'),('public', 'schedule'),('public', 'schema_migrations')])

    # Remove
    ok = srvPg.remove()
    self.assertEqual(ok, True)
    
    res = srvPg.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()
