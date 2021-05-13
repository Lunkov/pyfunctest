#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import git
import shutil
import docker
import traceback
import ftplib
from dotenv import dotenv_values
from pprint import pprint

class FTP():
  ''' Class for work with FTP '''

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
  
  def getConnect(self, moduleName):
    """ Connect to postgresql database
        Attributes
        ----------
        moduleName : str
            name of module
    """
    host = 'localhost'
    if 'FTP_HOST' in self.config:
      host = self.config['FTP_HOST']
    port = '21'
    if 'FTP_PORT' in self.config:
      port = self.config['FTP_PORT']
    self.connect = "%s:%s" % (host, port)

    user = ''
    if 'FTP_USER' in self.config:
      user = self.config['FTP_USER']
    password = ''
    if 'FTP_PASSWORD' in self.config:
      password = self.config['FTP_PASSWORD']

    try:
      self.handle = ftplib.FTP()
      self.handle.connect(host, int(port))
      self.handle.login(user, password)
      self.handle.set_pasv(True)
      return self.handle
    except Exception as e:
      print("FATAL: Connect to FTP '%s': %s" % (self.connect, str(e)))
    return None

  def getDirList(self):
    return self.handle.nlst()

  def cdTree(self, currentDir):
    if currentDir != '':
      try:
        self.handle.cwd(currentDir)
        print("DBG: 1 currentDir(%s)" % (currentDir))
      except Exception as e:
        self.cdTree("/".join(currentDir.split("/")[:-1]))
        self.handle.mkd(currentDir)
        self.handle.cwd(currentDir)
        print("DBG: 2 currentDir(%s): %s" % (currentDir, str(e)))

  def uploadFile(self, pathFTP, filename, fullPath):
    try:
      self.handle.cwd('/')
      self.cdTree(pathFTP)
      fileh = open(fullPath, 'rb')  
      self.handle.storbinary(f'STOR {filename}', fileh)
      fileh.close()
    except Exception as e:
      print("FATAL: uploadFile to FTP(%s): %s" % (self.connect, str(e)))
      return False
    return True

  def downloadFile(self, pathFTP, filename, fullPath):
    try:
      self.handle.cwd('/')
      self.cdTree(pathFTP)
      self.handle.retrbinary("RETR " + filename, open(fullPath, 'wb').write)
    except Exception as e:
      print("FATAL: downloadFile to FTP(%s): %s" % (self.connect, str(e)))
      return False
    return True

  def compareFiles(self, pathFTP, filename, filePath):
    result = False
    if not os.path.exists(filePath):
      return result
    try:
      pathTmp = os.path.join(self.pathTmp, pathFTP)
      os.makedirs(pathTmp, exist_ok=True)
      file1 = os.path.join(pathTmp, filename)
      self.handle.cwd('/')
      self.cdTree(pathFTP)
      self.handle.retrbinary("RETR " + filename, open(file1, 'wb').write)
      result = filecmp.cmp(file1, filePath, shallow=False)
      os.remove(file1)
    except Exception as e:
      print("FATAL: compareFiles FTP(%s): %s" % (self.connect, str(e)))
      return False
    return result
