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

    self.host = 'localhost'
    if 'DB_HOST' in self.config:
      self.host = self.config['DB_HOST']
    self.port = '5432'
    if 'DB_PORT' in self.config:
      self.port = self.config['DB_PORT']

    try:
      self.dbConn = psycopg2.connect(host=self.host,
                                port=self.port,
                                user=self.config['DB_USER'],
                                password=self.config['DB_PASSWORD'],
                                dbname=self.config['DB_NAME'])
      return self.dbConn
    except Exception as e:
      print("FATAL: Connect to DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return None

  def getTableList(self, schema = 'public'):
    # Retrieve the table list
    s = "SELECT table_schema, table_name FROM information_schema.tables WHERE (table_schema = '%s') ORDER BY table_schema, table_name;" % schema
    try:
      cursor = self.dbConn.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(s)
      return cursor.fetchall()
    except Exception as e:
      print("FATAL: getTableList DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return []

  def loadSQL(self, fileName):
    try:
      cursor = self.dbConn.cursor()
      sqlFile = open(fileName,'r')
      cursor.execute(sqlFile.read())
      return True
    except Exception as e:
      print("FATAL: loadSQL DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return False

  def getData(self, sql, schema = 'public'):
    # Retrieve the table list
    try:
      cursor = self.dbConn.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(sql)
      return cursor.fetchall()
    except Exception as e:
      print("FATAL: getTableList DB '%s:%s\\%s': %s" % (self.host, self.port, self.config['DB_NAME'], str(e)))
    return []
