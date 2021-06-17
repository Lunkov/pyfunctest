#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import ftplib
import filecmp
import socket
import errno
import pprint

class CustomFTP(ftplib.FTP):

  def makepasv(self):
    if self.af == socket.AF_INET:
      host, port = ftplib.parse227(self.sendcmd('PASV'))
    else:
      host, port = ftplib.parse229(self.sendcmd('EPSV'), self.sock.getpeername())

    if '0.0.0.0' == host:
      """ this ip will be unroutable, we copy Filezilla and return the host instead """
      host = self.host
    return host, port

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
    self.host = 'localhost'
    if 'FTP_HOST' in self.config:
      self.host = self.config['FTP_HOST']
    self.port = '21'
    if 'FTP_PORT' in self.config:
      self.port = self.config['FTP_PORT']
    self.port = int(self.port)

    self.user = ''
    if 'FTP_USER' in self.config:
      self.user = self.config['FTP_USER']
    self.password = ''
    if 'FTP_PASSWORD' in self.config:
      self.password = self.config['FTP_PASSWORD']

    self.url = "ftp://%s@%s:%d" % (self.user, self.host, self.port)

    self.handle = None
  
  def getConnect(self):
    """ Connect to FTP
    """
    return self.reconnect()
    
  def reconnect(self):
    self.close()
    timeout = 20
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while (self.handle is None) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      try:
        self.handle = CustomFTP()
        self.handle.connect(self.host, self.port, timeout=30)
        self.handle.login(self.user, self.password)
        self.handle.set_pasv(True)
          
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to FTP '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)

    if self.handle is None:
      print("FATAL: Connect to FTP '%s': %s" % (self.url, str_err))
      return None    
    
    if self.verbose:
      print("DBG: Connected to FTP '%s': %s" % (self.url, self.handle.getwelcome()))
    return self.handle
    
  def close(self):
    if not self.handle is None:
      self.handle.close()
    self.handle = None

  def getDirList(self, currentDir):
    res = []
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()
      try:
        res = self.handle.nlst(currentDir)
        elapsed_time += timeout
      except ftplib.error_perm as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to FTP '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to FTP '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)
        
    if len(str_err) > 0:
      print("ERR: getDirList(%s/%s): %s" % (self.url, currentDir, str_err))
      return res

    res.sort()
    
    if self.verbose:
      print("DBG: Directory list FTP '%s:%s': %s" % (self.url, currentDir, str(res)))
    return res

  def getFileList(self, currentDir):
    res = []
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()
      try:
        res = self.handle.nlst(currentDir)
        elapsed_time += timeout
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to FTP '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)
        
    if len(str_err) > 0:
      print("ERR: getFileList(%s/%s): %s" % (self.url, currentDir, str_err))
      return res

    res.sort()
    if self.verbose:
      print("DBG: File list FTP '%s:%s': %s" % (self.url, currentDir, str(res)))
    
    return res

  def init(self):
    if not 'INIT_FTP_CREATE_FOLDERS' in self.config:
      return
    folders = self.config['INIT_FTP_CREATE_FOLDERS']
    af = folders.split(';')
    for folder in af:
      self.mkDir(folder)

  def cd(self, currentDir):
    self.reconnect()
    self.handle.cwd('/')
    if currentDir != '':
      self.cdTree(currentDir, False)
      try:
        self.handle.cwd(currentDir)
      except Exception as e:
        print("ERR: Change Directory(%s/%s): %s" % (self.url, currentDir, str(e)))
    return self.handle.pwd() == currentDir

  def mkDir(self, currentDir):
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()
      self.handle.cwd('/')
      if currentDir != '':
        self.cdTree(currentDir)
        try:
          self.handle.cwd(currentDir)
          elapsed_time += timeout
        except Exception as e:
          print("ERR: Change Directory(%s/%s): %s" % (self.url, currentDir, str(e)))
          pprint.pprint(e)

    res = self.handle.pwd() == currentDir
    self.handle.cwd('/')
    return res

  def cdTree(self, currentDir, mk = True):
    if currentDir != '':
      try:
        self.handle.cwd(currentDir)
      except Exception as e:
        if self.verbose:
          print("DBG: Change Subdirectory(%s/%s): %s" % (self.url, currentDir, str(e)))
        self.cdTree("/".join(currentDir.split("/")[:-1]), mk)
        try:
          if mk:
            self.handle.mkd(currentDir)
        except Exception as e:
          print("ERR: Make Subdirectory(%s/%s): %s" % (self.url, currentDir, str(e)))
  
  def uploadFile(self, pathFTP, filename, fullPath):
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()
      try:
        str_err = ''
        self.handle.cwd('/')
        self.cdTree(pathFTP)
        fileh = open(fullPath, 'rb')  
        self.handle.storbinary(f'STOR {filename}', fileh)
        fileh.close()
        elapsed_time += timeout
      except Exception as e:
        print("FATAL: uploadFile to FTP(%s): %s" % (self.url, str(e)))
        str_err = str(e)
    if str_err != '':
      return False
    return True

  def downloadFile(self, pathFTP, filename, fullPath):
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()    
      try:
        str_err = ''
        self.handle.cwd('/')
        self.cdTree(pathFTP)
        self.handle.retrbinary("RETR " + filename, open(fullPath, 'wb').write)
        elapsed_time += timeout
      except Exception as e:
        print("FATAL: downloadFile to FTP(%s): %s" % (self.url, str(e)))
        str_err = str(e)

    if str_err != '':
      return False
    return True

  def compareFiles(self, pathFTP, filename, filePath):
    result = False
    if not os.path.exists(filePath):
      print("ERR: compareFiles FTP(%s): Local File not found: %s" % (self.url, filePath))
      return result
    try:
      pathTmp = os.path.join(self.pathTmp, pathFTP)
      os.makedirs(pathTmp, exist_ok=True)
      file1 = os.path.join(pathTmp, filename)
    except Exception as e:
      print("FATAL: compareFiles Local(%s): %s" % (self.url, str(e)))
      return False
    timeout = 15
    stop_time = 1
    elapsed_time = 0
    str_err = ''
    while elapsed_time < timeout:
      if elapsed_time > 0:
        time.sleep(stop_time)
      elapsed_time += stop_time
      self.reconnect()
      try:
        str_err = ''
        self.handle.cwd('/')
        self.cdTree(pathFTP)
        self.handle.retrbinary("RETR " + filename, open(file1, 'wb').write)
        result = filecmp.cmp(file1, filePath, shallow=False)
        os.remove(file1)
        elapsed_time += timeout
      except Exception as e:
        print("FATAL: compareFiles FTP(%s): %s" % (self.url, str(e)))
        str_err = str(e)

    if str_err != '':
      return False
    return result
