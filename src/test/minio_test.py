#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import requests
import time
from src.fmods import FMods

class TestMINIO(unittest.TestCase):

  def testFModsMINIO(self):
    fm = FMods("data/mods/", "data/tmp/", True)

    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('minio'), {})
    self.assertEqual(fm.getTmpFolder('minio'), 'data/tmp/git/minio')

    fm.scan()
    self.assertTrue(fm.count() > 7)

    #config_need = dict(sorted({('CONTAINER_NAME', 'minio-test'), ('CONTAINER_ENV_S3_ACCESS_KEY', 'user'), ('CONTAINER_ENV_S3_SECRET_KEY', 'pwd'), ('CONTAINER_PORTS', '3010:9000'), ('CONTAINER_SRC', 'minio/minio'), ('S3_ACCESS_KEY', 'user'), ('S3_SECRET_KEY', 'pwd'), ('NAME', 'minio'), ('TYPE', 'docker'), ('S3_PORT', '3010')}))
    #cfg = fm.getConfig('minio')
    #cfg.pop('MOD_PATH', None)
    #self.assertEqual(cfg, config_need)
    
    minio = fm.newMinIO('minio')
    
    conn = minio.getConnect()
    self.assertIsNone(conn)

    # Start service
    srvMINIO = fm.newDocker('minio')

    self.assertTrue(srvMINIO.run())
    self.assertEqual(srvMINIO.status(), 'running')

    time.sleep(5)

    # Test connect
    conn = minio.getConnect()
    self.assertIsNotNone(conn)

    self.assertEqual(minio.getBasketsList(), [])
    
    self.assertTrue(minio.uploadFile('bucket-test', 'test.txt', 'data/files/test.txt'))

    self.assertTrue(minio.downloadFile('bucket-test', 'test.txt', 'data/files/test2.txt'))
    self.assertTrue(minio.compareFiles('bucket-test', 'test.txt', 'data/files/test2.txt'))
    os.remove('data/files/test2.txt')

    self.assertTrue(minio.compareFiles('bucket-test', 'test.txt', 'data/files/test.txt'))
    self.assertFalse(minio.compareFiles('bucket-test1', 'test.txt', 'data/files/test2.txt'))
    self.assertFalse(minio.compareFiles('bucket-test', 'test.txt', 'data/files/test1.txt'))
    self.assertFalse(minio.compareFiles('bucket-test', 'test1.txt', 'data/files/test.txt'))

    self.assertEqual(minio.getBasketsList(), ['bucket-test'])

    # Remove
    self.assertTrue(srvMINIO.remove())
    self.assertEqual(srvMINIO.status(), 'not found')


if __name__ == '__main__':
  unittest.main()
