#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import docker
import git
import time
from .lfs import LFS
from .fmod import FMod

class Migrate(FMod):
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
    super(Migrate, self).__init__(config, pathTmp, verbose)

    self.networkName = 'test-net'
    if 'docker' in self.config:
      if 'network' in self.config['docker']:
        self.networkName = self.config['docker']['network']
    
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
    
  def isMigrate(self):
    """ Get parameters of module for Migrate
        Returns
        -------
        ok
            success
    """
    if 'migrate' in self.config:
      if 'command' in self.config['migrate']:
        return True
    return False
    

  def run(self):
    """ Migrate for Database container
    """
    if not self.isDocker():
      print("ERR: Docker run: Not Found (mod='%s')" % self.moduleName)
      return False
    if not self.isMigrate():
      print("ERR: Migrate run: Not Found (mod='%s')" % self.moduleName)
      return False
    
    if 'git_src' in self.config['migrate']:
      LFS.rm(self.pathTmp)
      if self.verbose:
        print("DBG: git.Clone(%s): %s => %s" % (self.moduleName, self.config['migrate']['git_src'], self.pathTmp))
      repo = git.Repo.clone_from(self.config['migrate']['git_src'], self.pathTmp, branch=self.config['migrate']['git_src'])

    # image: migrate/migrate
    # command: --path=/migrations/ --database="postgres://user:pwd@db_host:5432/db_name?sslmode=disable" up
    # volumes:
    #  - ./migrations:/migrations
    
    image = 'migrate/migrate'
    if 'image' in self.config['migrate']:
      image = self.config['migrate']['image']
    
    command = self.config['migrate']['command']
    
    # Volumes
    volumes = dict()
    vm = self.pathTmp
    if 'path' in self.config['migrate']:
      if 'git_src' in self.config['migrate']:
        vm = os.path.join(self.pathTmp, self.config['migrate']['path'])
      else:
        vm = os.path.join(self.config['mod_path'], self.config['migrate']['path'])
    vmi = '/migrations'
    if 'image_path' in self.config['migrate']:
      vmi = self.config['migrate']['image_path']
    if not os.path.isdir(vm):
      print("FATAL: Path for migrate is not exists: '%s:%s'" % (self.moduleName, vm))
      return False
      
    volumes[vm] = {'bind': vmi, 'mode': 'ro'}

    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    if 'timeout_before_migrate' in self.config['migrate']:
      time.sleep(self.config['migrate']['timeout_before_migrate'])
    
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
      if result:
        for s in result.decode('utf-8').split():
          print("ERR: Migrate(%s) '%s': %s" % (self.moduleName, image, s)) 
      return False
      
    return True
