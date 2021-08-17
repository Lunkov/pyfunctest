#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

from .fmod import FMod

class FModDB(FMod):
  ''' Class for environment module for functional tests '''

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
    super(FModDB, self).__init__(config, pathTmp, verbose)
    
    self.dbName = 'test-db'
    self.url = "db://%s@%s:%s/%s" % (self.user, self.host, self.port, self.dbName)

  def initConfig(self):
    if not 'db' in self.config:
      return
    
    if 'host' in self.config['db']:
      self.host = self.config['db']['host']
    if 'port' in self.config['db']:
      self.port = int(self.config['db']['port'])
    if 'name' in self.config['db']:
      self.dbName = self.config['db']['name']
    if 'user' in self.config['db']:
      self.user = self.config['db']['user']
    if 'password' in self.config['db']:
      self.password = self.config['db']['password']

  def loadSQL(self, fileName):
    try:
      cursor = self.handle.cursor()
      sqlFile = open(fileName,'r')
      cursor.execute(sqlFile.read())
      return True
    except Exception as e:
      print("FATAL: loadSQL DB '%s': %s" % (self.url, str(e)))
    return False

  def getData(self, sql, schema = 'public'):
    # Retrieve the table list
    try:
      cursor = self.handle.cursor()
      # Retrieve all the rows from the cursor
      cursor.execute(sql)
      return cursor.fetchall()
    except Exception as e:
      print("FATAL: getTableList DB '%s': %s" % (self.url, str(e)))
    return []
