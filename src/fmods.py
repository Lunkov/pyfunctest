#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import shutil
import traceback
import docker
from dotenv import dotenv_values
from pprint import pprint
from .docker import Docker
from .git import GIT
from .ftp import FTP
from .postgre import Postgre
from .mysql import MySQL
from .rabbitmq import RabbitMQ
from .kafka import Kafka

class FMods(object):
  ''' Class for load and build environment modules for functional tests '''

  def __init__ (self, pathModules, pathTmp, verbose):
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
    os.makedirs(self.pathTmp, exist_ok=True)
    if self.pathTmp == "":
      self.pathTmp = os.path.join(os.getcwd(), 'tmp')
    self.modules = dict()
    try:
      self.docker = docker.from_env()
      info = self.docker.version()
      if self.verbose:
        print("DBG: docker.version %s" % (info['Components'][0]['Version']))
    except:
      print("FATAL: Docker Not Found")
      sys.exit(1)
  
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
        config = dotenv_values(os.path.join(fullPath, ".env"))
        if "NAME" in config:
          if self.verbose:
            print("DBG: find mod: %s" % config['NAME'])
          name = config['NAME']
          config['MOD_PATH'] = fullPath
          self.modules[name] = set()
          self.modules[name] = dict(sorted(config.items()))
        else:
          if self.verbose:
            print("WRN: Module not found in %s" % fullPath)

  def printList(self):
    """ Output the list of modules
    """
    for name, _ in self.modules.items():
      print("LOG: mod: %s" % name)

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

  def startAll(self):
    """ setUp for UTests
    """
    for moduleName, config in self.modules.items():
      if 'GIT_SRC' in config:
        self.gitClone(moduleName)
      self.dockerRemove(moduleName)
      if 'DOCKERFILE' in config:
        self.dockerBuild(moduleName)
        self.dockerRun(moduleName)
      else:
        if 'CONTAINER_SRC' in config:
          self.dockerRun(moduleName)


  def stopAll(self):
    """ tearDown for UTests
    """
    shutil.rmtree(self.pathTmp, ignore_errors=True)
    for moduleName, config in self.modules.items():
      self.dockerRemove(moduleName)

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

  def newRabbitMQ(self, moduleName):
    return RabbitMQ(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)

  def newKafka(self, moduleName):
    return Kafka(self.getConfig(moduleName), self.getTmpFolder(moduleName), self.verbose)
