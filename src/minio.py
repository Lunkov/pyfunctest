#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import io
import sys
import time
import filecmp
from minio import Minio
from .fmod import FMod

class MinIO(FMod):
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
    super(MinIO, self).__init__(config, pathTmp, verbose)

    self.port = 9000
    self.access_key = ''
    self.secret_key = ''
    if 's3' in self.config:
      if 'host' in self.config['s3']:
        self.host = self.config['s3']['host']
      if 'port' in self.config['s3']:
        self.port = int(self.config['s3']['port'])
      if 'access_key' in self.config['s3']:
        self.access_key = self.config['s3']['access_key']
      if 'secret_key' in self.config['s3']:
        self.secret_key = self.config['s3']['secret_key']
    self.url = "%s:%d" % (self.host, self.port)
      
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

  def init(self):
    if not 's3' in self.config:
      return
    if not 'init' in self.config['s3']:
      return
    if not 'create_folders' in self.config['s3']['init']:
      return
    if self.reconnect() is None:
      return
    folders = self.config['s3']['init']['create_folders']
    for folder in folders:
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
      if self.verbose:
        print("DBG: Make folder '%s:%s' into Minio(%s)" % (bucketName, fullPath, self.url))
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
