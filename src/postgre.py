#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import psycopg2
from .fmod_db import FModDB

class Postgre(FModDB):
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
    super(Postgre, self).__init__(config, pathTmp, verbose)

    self.user = 'user'
    self.port = 5432
    self.dbName = 'test-db'

    self.initConfig()

    self.url = "pg://%s@%s:%d/%s" % (self.user, self.host, self.port, self.dbName)
  
  
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
        self.handle = psycopg2.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        dbname=self.dbName)
          
      except Exception as e:
        if self.verbose:
          print("DBG: WAIT: %d: Connect to PostgreSQL '%s':%s" % (elapsed_time, self.url, str(e)))
        str_err = str(e)

    if self.handle is None:
      print("FATAL: Connect to PostgreSQL '%s': %s" % (self.url, str_err))
      return None    
    
    if self.verbose:
      print("DBG: Connected to PostgreSQL '%s'" % (self.url))
    return self.handle
    
  def getTableList(self, schema = 'public'):
    # Retrieve the table list
    s = "SELECT table_schema, table_name FROM information_schema.tables WHERE (table_schema = '%s') ORDER BY table_schema, table_name;" % schema
    try:
      cursor = self.handle.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(s)
      return cursor.fetchall()
    except Exception as e:
      print("FATAL: getTableList DB '%s': %s" % (self.url, str(e)))
    return []

