#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import time
import os
from src.fmods import FMods

class TestFTP(unittest.TestCase):

  def testFModsFTP(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('ftp'), {})
    self.assertEqual(fm.getTmpFolder('ftp'), 'data/tmp/git/ftp')

    fm.scan()
    self.assertTrue(fm.count() > 1)

    # Start service
    srvFTP = fm.newDocker('ftp')

    self.assertTrue(srvFTP.run())
    self.assertEqual(srvFTP.status(), 'running')

    ftp = fm.newFTP('ftp')
    
    conn = ftp.reconnect()
    self.assertIsNotNone(conn)

    self.assertEqual(ftp.getDirList(''), ['incoming'])
    self.assertEqual(ftp.getFileList(''), ['incoming'])
    self.assertFalse(ftp.cd('incoming'))
    self.assertFalse(ftp.cd('incoming2'))
    self.assertTrue(ftp.mkDir('/folder-test/folder-test2'))

    self.assertEqual(ftp.getFileList('/folder-test'), ['/folder-test/folder-test2'])
    self.assertTrue(ftp.uploadFile('folder-test', 'test.txt', 'data/files/test.txt'))
    self.assertEqual(ftp.getFileList('/folder-test'), ['/folder-test/folder-test2', '/folder-test/test.txt'])
    
    self.assertTrue(ftp.downloadFile('folder-test', 'test.txt', 'data/files/test2.txt'))
    self.assertTrue(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test2.txt'))
    os.remove('data/files/test2.txt')

    self.assertTrue(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test.txt'))
    self.assertFalse(ftp.compareFiles('folder-test1', 'test.txt', 'data/files/test2.txt'))
    self.assertFalse(ftp.compareFiles('folder-test', 'test.txt', 'data/files/test1.txt'))
    self.assertFalse(ftp.compareFiles('folder-test', 'test1.txt', 'data/files/test.txt'))

    self.assertEqual(ftp.getDirList(''), ['folder-test', 'incoming'])
    
    ftp.init()
    self.assertEqual(ftp.getDirList(''), ['folder-test', 'folder-test1', 'incoming'])
    
    # Remove
    ok = srvFTP.remove()
    self.assertEqual(ok, True)
    
    res = srvFTP.status()
    self.assertEqual(res, 'not found')


if __name__ == '__main__':
  unittest.main()
