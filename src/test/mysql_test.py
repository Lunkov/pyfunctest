#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
from src.fmods import FMods

class TestMySql(unittest.TestCase):

  def testFModsMySQL(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('mysql'), {})
    self.assertEqual(fm.getTmpFolder('mysql'), 'data/tmp/git/mysql')

    fm.scan()
    self.assertTrue(fm.count() > 7)

    #config_need = dict(sorted({('CONTAINER_NAME', 'mysql-test'), ('CONTAINER_ENV_MYSQL_DATABASE', 'test-db'), ('CONTAINER_ENV_MYSQL_PASSWORD', 'pwd'), ('CONTAINER_ENV_MYSQL_ROOT_PASSWORD', 'pwd'), ('CONTAINER_ENV_MYSQL_USER', 'user'), ('CONTAINER_PORTS', '17436:3306'), ('CONTAINER_SRC', 'mysql'), ('DB_NAME', 'test-db'), ('DB_PASSWORD', 'pwd'), ('DB_USER', 'root'), ('NAME', 'mysql'), ('TYPE', 'docker'), ('DB_PORT', '17436')}))
    #cfg = fm.getConfig('mysql')
    #cfg.pop('MOD_PATH', None)
    #self.assertEqual(cfg, config_need)
    
    msql = fm.newMySQL('mysql')
    
    dbconn = msql.reconnect()
    self.assertIsNone(dbconn)

    # Start service
    srvMySQL = fm.newDocker('mysql')

    ok = srvMySQL.run()
    self.assertTrue(ok)
    res = srvMySQL.status()
    self.assertEqual(res, 'running')

    time.sleep(2)

    # Test connect
    dbconn = msql.reconnect()
    self.assertIsNotNone(dbconn)
    tbl = msql.getTableList()
    self.assertEqual(tbl, [])

    self.assertTrue(msql.loadSQL('data/mysql/create_table.sql'))

    tbl = msql.getTableList()
    self.assertEqual(tbl, ['article'])

    self.assertTrue(msql.loadSQL('data/mysql/create_tables.sql'))
    
    tbl = msql.getTableList()
    self.assertEqual(tbl, ['article', 'article2', 'article3'])
    
    res = msql.getData('select * from public.article')
    self.assertEqual(res, [])
    
    self.assertTrue(msql.loadSQL('data/mysql/insert.sql'))
    res = msql.getData('select * from article')
    self.assertEqual(res, ((1, 'article 1', 'description'),))

    # Remove
    ok = srvMySQL.remove()
    self.assertEqual(ok, True)
    
    res = srvMySQL.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()
