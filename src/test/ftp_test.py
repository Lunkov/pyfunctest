#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
import os
from src.fmods import FMods
from src.docker import Docker
from src.ftp import FTP

class TestFTP(unittest.TestCase):

  def testFModsFTP(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('ftp'), {})
    self.assertEqual(fm.getTmpFolder('ftp'), 'data/tmp/git/ftp')

    fm.scan()
    self.assertEqual(fm.count(), 7)

    #config_need = dict(sorted({('CONTAINER_NAME', 'ftp-test'), ('CONTAINER_ENV_FTP_PASSWORD', 'pwd'), ('CONTAINER_ENV_FTP_USER', 'user'), ('CONTAINER_PORTS', '3021:21'), ('CONTAINER_SRC', 'teezily/ftpd'), ('FTP_PASSWORD', 'pwd'), ('FTP_USER', 'user'), ('NAME', 'ftp'), ('TYPE', 'docker'), ('FTP_PORT', '3021')}))
    #cfg = fm.getConfig('ftp')
    #cfg.pop('MOD_PATH', None)
    #self.assertEqual(cfg, config_need)
    
    ftp = FTP(fm.getConfig('ftp'), fm.getTmpFolder('ftp'), True)
    
    conn = ftp.getConnect('ftp')
    self.assertIsNone(conn)

    # Start service
    srvFTP = Docker(fm.getConfig('ftp'), fm.getTmpFolder('ftp'), True)

    ok = srvFTP.run()
    self.assertTrue(ok)
    res = srvFTP.status()
    self.assertEqual(res, 'running')

    time.sleep(5)

    # Test connect
    conn = ftp.getConnect('ftp')
    self.assertIsNotNone(conn)
    tbl = ftp.getDirList()
    self.assertEqual(tbl, ['incoming'])

    self.assertTrue(ftp.uploadFile('folder-test', 'test.txt', 'data/files/test.txt'))

    self.assertTrue(ftp.downloadFile('folder-test', 'test.txt', 'data/files/test2.txt'))
    self.assertTrue(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test2.txt'))
    os.remove('data/files/test2.txt')

    self.assertTrue(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test.txt'))
    self.assertFalse(ftp.compareFiles('folder-test1', 'test.txt', 'data/files/test2.txt'))
    self.assertFalse(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test1.txt'))
    self.assertFalse(ftp.compareFiles('folder-test', 'test1.txt', 'data/files/test.txt'))

    tbl = ftp.getDirList()
    self.assertEqual(tbl, ['folder-test', 'incoming'])
    
    
    # Remove
    ok = srvFTP.remove()
    self.assertEqual(ok, True)
    
    res = srvFTP.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()