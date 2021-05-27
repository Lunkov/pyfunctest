#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import MySQLdb
import traceback

class MySQL(object):
  ''' Class for work with DB '''

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
    self.host = '127.0.0.1'
    if 'DB_HOST' in self.config:
      self.host = self.config['DB_HOST']
    self.port = 3306
    if 'DB_PORT' in self.config:
      self.port = int(self.config['DB_PORT'])
    self.dbName = 'test-db'
    if 'DB_NAME' in self.config:
      self.dbName = self.config['DB_NAME']
    self.user = 'user'
    if 'DB_USER' in self.config:
      self.user = self.config['DB_USER']
    self.password = ''
    if 'DB_PASSWORD' in self.config:
      self.password = self.config['DB_PASSWORD']

    self.url = "mysql://%s@%s:%d/%s" % (self.user, self.host, self.port, self.dbName)
    self.handle = None

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
        self.handle = MySQLdb.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    passwd=self.password,
                                    db=self.dbName,
                                    database=self.dbName)
          
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to MySQL '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)

    if self.handle is None:
      print("FATAL: Connect to MySQL '%s': %s" % (self.url, str_err))
      return None    
    
    if self.verbose:
      print("DBG: Connected to MySQL '%s'" % (self.url))
    return self.handle
    
  def close(self):
    if not self.handle is None:
      self.handle.close()
    self.handle = None

  def getTableList(self):
    # Retrieve the table list
    s = "SHOW TABLES;"
    try:
      cursor = self.handle.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(s)
      res = []
      for b in cursor.fetchall():
        res.append(b[0])
      res.sort()
      return res      
    except Exception as e:
      print("FATAL: getTableList DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return []

  def loadSQL(self, fileName):
    try:
      cursor = self.handle.cursor()
      sqlFile = open(fileName,'r')
      cursor.execute(sqlFile.read())
      return True
    except Exception as e:
      print("FATAL: loadSQL DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return False

  def getData(self, sql):
    # Retrieve the table list
    try:
      cursor = self.handle.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(sql)
      return cursor.fetchall()
    except Exception as e:
      print("FATAL: getTableList DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return []
