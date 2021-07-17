#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import yaml

from .docker import Docker
from .git import GIT
from .ftp import FTP
from .minio import MinIO
from .postgre import Postgre
from .mysql import MySQL
from .migrate import Migrate
from .rabbitmq import RabbitMQ
from .kafka import Kafka
from .http import HTTP
from .httpserver import HTTPSrv
from .lfs import LFS

class FMods(object):
  ''' Class for load and build environment modules for functional tests '''

  def __init__ (self, pathModules, pathTmp = '', verbose = True):
    """ Initialising object
    Parameters
    ----------
    pathModules : str
        path to modules settings
    pathTmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.pathModules = os.path.abspath(pathModules)
    self.pathTmp = pathTmp
    if self.pathTmp == '':
      self.pathTmp = os.path.join(os.getcwd(), 'tmp')
    os.makedirs(self.pathTmp, exist_ok=True)
    self.modules = dict()
  
  def scan(self):
    """ Scan subfolders for modules settings (path_modules)
    """
    if self.verbose:
      print("DBG: scan folder: %s" % self.pathModules)
    lstDir = ''
    try:
      lstDir = os.listdir(self.pathModules)
    except:
      print("FATAL: Folder Not Found: %s" % (self.pathModules))

    for curDir in lstDir:
      if self.verbose:
        print("DBG: scan subfolder: %s" % curDir)
      fullPath = os.path.join(self.pathModules, curDir)
      if os.path.isdir(fullPath):
        with open(os.path.join(fullPath, ".yaml"), 'r') as stream:
          try:
            config = yaml.safe_load(stream)
            if 'name' in config:
              if self.verbose:
                print("DBG: find mod: %s" % config['name'])
              name = config['name']
              config['mod_path'] = fullPath
              if not 'order' in config:
                config['order'] = 0
              else:
                config['order'] = int(config['order'])
              self.modules[name] = set()
              self.modules[name] = dict(sorted(config.items()))
            else:
              if self.verbose:
                print("WRN: Module not found in %s" % fullPath)
          except yaml.YAMLError as exc:
            print("ERR: Bad format in %s: %s" % (fullPath, exc))


  def printList(self):
    """ Output the list of modules
    """
    for s in sorted(self.modules.items(), key=lambda k_v: k_v[1]['order']):
      print("LOG: mod: %s \t (order=%d)" % (s[1]['name'], s[1]['order']))

  def count(self):
    """ Count of modules
    """
    return len(self.modules)

  def getConfig(self, moduleName):
    """ Get configuration of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    return self.modules.get(moduleName, {})

  def getTmpFolder(self, moduleName):
    """ Get temporary path for module
        Parameters
        ----------
        moduleName : str
            name of the module
            
        Returns
        -------
        path:
            temporary path for the module
    """
    return os.path.join(self.pathTmp, 'git', moduleName)

  def _gitClone(self, config, moduleName):
    if 'git' in config:
      if 'src' in config['git']:
        gt = self.newGIT(moduleName)
        gt.clone()

  def _dockerBuild(self, config, moduleName):
    if 'docker' in config:
      if 'dockerfile' in config['docker']:
        srv = self.newDocker(moduleName)
        srv.build(False)
        srv.run(False)
        srv.statusWaiting('running')

  def _dockerRun(self, config, moduleName):
    if 'docker' in config:
      if 'src' in config['docker']:
        srv = self.newDocker(moduleName)
        srv.run()
        srv.statusWaiting('running')

  def _dockerCompose(self, config, moduleName):
    if 'docker' in config:
      if 'compose' in config['docker']:
        srv = self.newDocker(moduleName)
        srv.startCompose()

  def _migrate(self, config, moduleName):
    if 'migrate' in config:
      if 'command' in config['migrate']:
        migrate = self.newMigrate(moduleName)
        migrate.run()

  def _init(self, config, moduleName):
    if 'rabbitmq' in config:
      if 'init' in config['rabbitmq']:
        srv = self.newRabbitMQ(moduleName)
        srv.init()
    if 'kafka' in config:
      if 'init' in config['kafka']:
        srv = self.newKafka(moduleName)
        srv.init()
    if 's3' in config:
      if 'init' in config['s3']:
        srv = self.newMinIO(moduleName)
        srv.init()
    if 'ftp' in config:
      if 'init' in config['ftp']:
        srv = self.newFTP(moduleName)
        srv.init()

  def startAll(self):
    """ setUp for UTests
    """
    operations = {
        'clone': self._gitClone,
        'run': self._dockerRun,
        'build': self._dockerBuild,
        'compose': self._dockerCompose,
        'migrate': self._migrate,
        'init': self._init,
    }      
    for s in sorted(self.modules.items(), key=lambda k_v: k_v[1]['order']):
      moduleName = s[1]['name']
      config = s[1]
      if 'actions' in config:
        seq = config['actions']
      else:
        seq = ['clone', 'build', 'compose', 'run', 'migrate']
      for s in seq:
        if s in operations:
          if self.verbose:
            print("DBG: Module(%s) Action: %s" % (moduleName, s))
          operations[s](config, moduleName)

  def stopAll(self):
    """ tearDown for UTests
    """
    LFS.rm(self.pathTmp)
    for s in sorted(self.modules.items(), key=lambda k_v: k_v[1]['order'], reverse=True):
      moduleName = s[1]['name']
      config = s[1]
      if 'docker' in config:
        if 'src' in config['docker']:
          srv = self.newDocker(moduleName)
          srv.remove()
        if 'compose' in config['docker']:
          srv = self.newDocker(moduleName)
          srv.stopCompose()

  def newDocker(self, moduleName):
    return Docker(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newGIT(self, moduleName):
    return GIT(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newFTP(self, moduleName):
    return FTP(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newMinIO(self, moduleName):
    return MinIO(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newMySQL(self, moduleName):
    return MySQL(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newPostgre(self, moduleName):
    return Postgre(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newMigrate(self, moduleName):
    return Migrate(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newRabbitMQ(self, moduleName):
    return RabbitMQ(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newKafka(self, moduleName):
    return Kafka(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newHTTP(self, moduleName):
    return HTTP(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newHTTPServer(self, moduleName):
    return HTTPSrv(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)
