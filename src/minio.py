#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import traceback
from minio import Minio

class MinIO(object):
  ''' Class for work with Minio '''

  def __init__ (self, config, pathTmp, verbose):
    """ Initialising object
    Parameters
    ----------
    config : dict
        config of module
    pathTmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.config = config
    self.pathTmp = pathTmp
    self.moduleName = self.config['NAME']
  
  def getConnect(self):
    """ Connect to minio
    """
    host = 'localhost'
    if 'S3_HOST' in self.config:
      host = self.config['S3_HOST']
    port = '9000'
    if 'S3_PORT' in self.config:
      port = self.config['S3_PORT']
    self.connect = "%s:%s" % (host, port)

    access_key = ''
    if 'S3_ACCESS_KEY' in self.config:
      access_key = self.config['S3_ACCESS_KEY']
    secret_key = ''
    if 'S3_SECRET_KEY' in self.config:
      secret_key = self.config['S3_SECRET_KEY']

    try:
      self.handle = Minio(self.connect, access_key=access_key,
                                secret_key=secret_key, secure=False)
                                
      self.handle.list_buckets()
      return self.handle
    except Exception as e:
      print("FATAL: Connect to Minio(%s): %s" % (self.connect, str(e)))
    return None

  def getBasketsList(self):
    bs = self.handle.list_buckets()
    res = []
    for b in bs:
      res.append(b.name)
    res.sort()
    return res

  def uploadFile(self, bucket, filename, fullPath):
    try:
      found = self.handle.bucket_exists(bucket)
      if not found:
          self.handle.make_bucket(bucket)
      self.handle.fput_object(bucket, filename, fullPath)
    except Exception as e:
      print("FATAL: uploadFile to Minio(%s): %s" % (self.connect, str(e)))
      return False
    return True

  def downloadFile(self, bucket, filename, fullPath):
    try:
      self.handle.fget_object(bucket, filename, fullPath)
    except Exception as e:
      print("FATAL: downloadFile to Minio(%s): %s" % (self.connect, str(e)))
      return False
    return True

  def compareFiles(self, bucket, filename, filePath):
    result = False
    if not os.path.exists(filePath):
      return result
    try:
      pathTmp = os.path.join(self.pathTmp, bucket)
      os.makedirs(pathTmp, exist_ok=True)
      file1 = os.path.join(pathTmp, filename)
      self.handle.fget_object(bucket, filename, file1)
      result = filecmp.cmp(file1, filePath, shallow=False)
      os.remove(file1)
    except Exception as e:
      print("FATAL: compareFiles Minio(%s): %s" % (self.connect, str(e)))
      return False
    return result
