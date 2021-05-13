#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import git
import shutil
import docker
import MySQLdb
import traceback
from dotenv import dotenv_values
from pprint import pprint

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
  
  def getConnect(self, moduleName):
    """ Connect to postgresql database
        Attributes
        ----------
        moduleName : str
            name of module
    """
    if not 'DB_NAME' in self.config:
      print("LOG: SQL: Module '%s'. DB_NAME Not Found" % (self.moduleName))
      return None
    if not 'DB_USER' in self.config:
      print("LOG: SQL: Module '%s'. DB_USER Not Found" % (self.moduleName))
      return None
    if not 'DB_PASSWORD' in self.config:
      print("LOG: SQL: Module '%s'. DB_PASSWORD Not Found" % (self.moduleName))
      return None

    host = '127.0.0.1'
    if 'DB_HOST' in self.config:
      host = self.config['DB_HOST']
    port = 3306
    if 'DB_PORT' in self.config:
      port = int(self.config['DB_PORT'])

    try:
      self.dbConn = MySQLdb.connect(host=host,
                                    port=port,
                                    user=self.config['DB_USER'],
                                    passwd=self.config['DB_PASSWORD'],
                                    db=self.config['DB_NAME'])
      return self.dbConn
    except Exception as e:
      print("FATAL: Connect to DB '%s:%s\\%s': %s" % (host, port, self.config['DB_NAME'], str(e)))
    return None

  def getTableList(self):
    # Retrieve the table list
    s = "SHOW TABLES"

    cursor = self.dbConn.cursor()
    # Retrieve all the rows from the cursor
    cursor.execute(s)
    return cursor.fetchall()

  def loadSQL(self, fileName):
    cursor = self.dbConn.cursor()
    sqlFile = open(fileName,'r')
    cursor.execute(sqlFile.read())
