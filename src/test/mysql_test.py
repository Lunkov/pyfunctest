#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
from src.fmods import FMods
from src.docker import Docker
from src.mysql import MySQL

class TestMySql(unittest.TestCase):

  def testFModsMySQL(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('mysql'), {})
    self.assertEqual(fm.getTmpFolder('mysql'), 'data/tmp/git/mysql')

    fm.scan()
    self.assertEqual(fm.count(), 7)

    config_need = dict(sorted({('CONTAINER_NAME', 'mysql-test'), ('CONTAINER_ENV_MYSQL_DATABASE', 'test-db'), ('CONTAINER_ENV_MYSQL_PASSWORD', 'pwd'), ('CONTAINER_ENV_MYSQL_ROOT_PASSWORD', 'pwd'), ('CONTAINER_ENV_MYSQL_USER', 'user'), ('CONTAINER_PORTS', '17436:3306'), ('CONTAINER_SRC', 'mysql'), ('DB_NAME', 'test-db'), ('DB_PASSWORD', 'pwd'), ('DB_USER', 'root'), ('NAME', 'mysql'), ('TYPE', 'docker'), ('DB_PORT', '17436')}))
    cfg = fm.getConfig('mysql')
    cfg.pop('MOD_PATH', None)
    self.assertEqual(cfg, config_need)
    
    msql = MySQL(fm.getConfig('mysql'), fm.getTmpFolder('mysql'), True)
    
    dbconn = msql.getConnect('mysql')
    self.assertIsNone(dbconn)

    # Start service
    srvMySQL = Docker(fm.getConfig('mysql'), fm.getTmpFolder('mysql'), True)

    ok = srvMySQL.run()
    self.assertTrue(ok)
    res = srvMySQL.status()
    self.assertEqual(res, 'running')

    time.sleep(15)

    # Test connect
    dbconn = msql.getConnect('mysql')
    self.assertIsNotNone(dbconn)
    tbl = msql.getTableList()
    self.assertEqual(tbl, [])

    self.assertTrue(msql.loadSQL('data/mysq/create_table.sql'))

    tbl = msql.getTableList()
    self.assertEqual(tbl, [])

    # Remove
    ok = srvMySQL.remove()
    self.assertEqual(ok, True)
    
    res = srvMySQL.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()
