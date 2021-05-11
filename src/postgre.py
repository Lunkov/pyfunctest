#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import git
import shutil
import docker
import psycopg2
import traceback
from dotenv import dotenv_values
from pprint import pprint

class Postgre(object):
  ''' Class for load and build environment modules for functional tests '''

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

    host = 'localhost'
    if 'DB_HOST' in self.config:
      host = self.config['DB_HOST']
    port = '5432'
    if 'DB_PORT' in self.config:
      port = self.config['DB_PORT']

    try:
      handle = psycopg2.connect(host=host,
                                port=port,
                                user=self.config['DB_USER'],
                                password=self.config['DB_PASSWORD'],
                                dbname=self.config['DB_NAME'])
      return handle
    except Exception as e:
      print("FATAL: Connect to DB '%s:%s\%s': %s" % (host, port, self.config['DB_NAME'], str(e)))
    return None

  def getTableList(dbCursor, schema = 'public'):
    # Retrieve the table list
    s = ""
    s += "SELECT"
    s += " table_schema"
    s += ", table_name"
    s += " FROM information_schema.tables"
    s += " WHERE"
    s += " ("
    s += " table_schema = '" + schema + "'"
    s += " )"
    s += " ORDER BY table_schema, table_name;"

    # Retrieve all the rows from the cursor
    dbCursor.execute(s)
    return dbCursor.fetchall()
