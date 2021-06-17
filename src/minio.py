#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import io
import sys
import time
import filecmp
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
    self.handle = None
    self.host = 'localhost'
    if 'S3_HOST' in self.config:
      self.host = self.config['S3_HOST']
    self.port = '9000'
    if 'S3_PORT' in self.config:
      self.port = self.config['S3_PORT']
    self.url = "%s:%s" % (self.host, self.port)
    self.access_key = ''
    if 'S3_ACCESS_KEY' in self.config:
      self.access_key = self.config['S3_ACCESS_KEY']
    self.secret_key = ''
    if 'S3_SECRET_KEY' in self.config:
      self.secret_key = self.config['S3_SECRET_KEY']
      
  def reconnect(self):
    self.close()
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while (self.handle is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.handle = Minio(self.url, access_key=self.access_key,
                                secret_key=self.secret_key, secure=False)
          
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to Minio '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)

    if self.handle is None:
      print("FATAL: Connect to Minio '%s': %s" % (self.url, str_err))
      return None    
    
    if self.verbose:
      print("DBG: Connected to Minio '%s'" % (self.url))
    return self.handle

  def close(self):
    if not self.handle is None:
      self.handle.close()
    self.handle = None

  def init(self):
    if not 'INIT_MINIO_CREATE_FOLDERS' in self.config:
      return
    folders = self.config['INIT_MINIO_CREATE_FOLDERS']
    af = folders.split(';')
    for folder in af:
      f = folder.split(':')
      if len(f) == 2:
        self.mkDir(f[0], f[1])    

  def getBasketsList(self):
    bs = self.handle.list_buckets()
    res = []
    for b in bs:
      res.append(b.name)
    res.sort()
    return res

  def uploadFile(self, bucketName, filename, fullPath):
    try:
      found = self.handle.bucket_exists(bucketName)
      if not found:
          self.handle.make_bucket(bucketName)
      self.handle.fput_object(bucketName, filename, fullPath)
    except Exception as e:
      print("FATAL: uploadFile to Minio(%s): %s" % (self.url, str(e)))
      return False
    return True

  def mkDir(self, bucketName, fullPath):
    try:
      found = self.handle.bucket_exists(bucketName)
      if not found:
          self.handle.make_bucket(bucketName)
      self.handle.put_object(bucketName, fullPath, io.BytesIO(b''), 0, content_type='application/x-directory')
    except Exception as e:
      print("FATAL: Make folder '%s' into Minio(%s): %s" % (fullPath, self.url, str(e)))
      return False
    return True
    
  def getListObjects(self, bucketName, currentDir=''):
    res = []
    objects = []
    try:
      found = self.handle.bucket_exists(bucketName)
      if not found:
          self.handle.make_bucket(bucketName)
      objects = self.handle.list_objects(bucketName, prefix=currentDir, recursive=True)
    except Exception as e:
      print("FATAL: List folder '%s' into Minio(%s): %s" % (currentDir, self.url, str(e)))
    for obj in objects:
      res.append(obj.object_name)
    return res

  def downloadFile(self, bucketName, filename, fullPath):
    try:
      self.handle.fget_object(bucketName, filename, fullPath)
    except Exception as e:
      print("FATAL: downloadFile to Minio(%s): %s" % (self.url, str(e)))
      return False
    return True

  def compareFiles(self, bucketName, filename, filePath):
    result = False
    if not os.path.exists(filePath):
      return result
    try:
      pathTmp = os.path.join(self.pathTmp, bucketName)
      os.makedirs(pathTmp, exist_ok=True)
      file1 = os.path.join(pathTmp, filename)
      self.handle.fget_object(bucketName, filename, file1)
      result = filecmp.cmp(file1, filePath, shallow=False)
      os.remove(file1)
    except Exception as e:
      print("FATAL: compareFiles Minio(%s): %s" % (self.url, str(e)))
      return False
    return result
