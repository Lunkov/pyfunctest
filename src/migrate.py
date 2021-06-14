#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import docker
import git
from .lfs import LFS

class Migrate(object):
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
    self.moduleName = 'undefined'
    if 'NAME' in self.config:
      self.moduleName = self.config['NAME']
    self.networkName = 'test-net'
    if 'CONTAINER_NETWORK' in self.config:
      self.networkName = self.config['CONTAINER_NETWORK']
    
    try:
      self.docker = docker.from_env()
      info = self.docker.version()
      if self.verbose:
        print("DBG: docker.version %s" % (info['Components'][0]['Version']))
    except:
      print("FATAL: Docker Not Found")
      sys.exit(1)

    net = None
    try:
      net = self.docker.networks.get(self.networkName)
    except:
      print("ERR: Docker network(%s) Not Found" % self.networkName)
    if net is None:
      self.docker.networks.create(self.networkName, driver="bridge")
    
  def isDocker(self):
    """ Get parameters of module for docker
        Returns
        -------
        ok
            success
    """
    return ('CONTAINER_NAME' in self.config)

  def run(self):
    """ Migrate for Database container
    """
    if not self.isDocker():
      print("ERR: Docker run: Not Found (mod='%s')" % self.moduleName)
      return False
    
    if not 'MIGRATE_COMMAND' in self.config:
      return False

    if 'MIGRATE_GIT_SRC' in self.config:
      LFS.rm(self.pathTmp)
      if self.verbose:
        print("DBG: git.Clone(%s): %s => %s" % (self.moduleName, self.config['MIGRATE_GIT_SRC'], self.pathTmp))
      repo = git.Repo.clone_from(self.config['MIGRATE_GIT_SRC'], self.pathTmp, branch=self.config['MIGRATE_GIT_BRANCH'])

    # image: migrate/migrate
    # command: --path=/migrations/ --database="postgres://user:pwd@db_host:5432/db_name?sslmode=disable" up
    # volumes:
    #  - ./migrations:/migrations
    
    image = 'migrate/migrate'
    if 'MIGRATE_IMAGE' in self.config:
      image = self.config['MIGRATE_IMAGE']
    
    command = self.config['MIGRATE_COMMAND']
    
    # Volumes
    volumes = dict()
    vm = self.pathTmp
    if 'MIGRATE_PATH' in self.config:
      if 'MIGRATE_GIT_SRC' in self.config:
        vm = os.path.join(self.pathTmp, self.config['MIGRATE_PATH'])
      else:
        vm = os.path.join(self.config['MOD_PATH'], self.config['MIGRATE_PATH'])
    vmi = '/migrations'
    if 'MIGRATE_IMAGE_PATH' in self.config:
      vmi = self.config['MIGRATE_IMAGE_PATH']
    if not os.path.isdir(vm):
      print("FATAL: Path for migrate is not exists: '%s:%s'" % (self.moduleName, vm))
      return False
      
    volumes[vm] = {'bind': vmi, 'mode': 'ro'}

    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    result = ''
    try:
      print("LOG: Docker: Run '%s' migrate: %s" % (image, command)) 
      if self.verbose:
        print("DBG: Docker: docker run -v %s:%s --network %s %s %s" % (vm, vmi, self.networkName, image, command)) 
      result = self.docker.containers.run(image, command=command, network=self.networkName, volumes=volumes, detach=False, auto_remove=True, stderr=True)
      if self.verbose and result:
        for s in result.decode('utf-8').split():
          print("DBG: Migrate(%s) '%s': %s" % (self.moduleName, image, s)) 
    except Exception as e:
      print("FATAL: Docker run migrate '%s:%s': %s" % (self.moduleName, image, str(e)))
      return False
      
    return True
