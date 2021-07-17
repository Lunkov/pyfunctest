#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import MySQLdb
from .fmod_db import FModDB

class MySQL(FModDB):
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
    super(MySQL, self).__init__(config, pathTmp, verbose)

    self.port = 3306
    self.user = 'user'

    self.initConfig()

    self.url = "mysql://%s@%s:%d/%s" % (self.user, self.host, self.port, self.dbName)

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
      print("FATAL: getTableList DB '%s': %s" % (self.url, str(e)))
    return []


