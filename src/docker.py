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

class Docker(object):
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
    if 'CONTAINER_NAME' in self.config:
      self.moduleName = self.config['NAME']
    else:
      self.moduleName = 'undefined'
    try:
      self.docker = docker.from_env()
      info = self.docker.version()
      if self.verbose:
        print("DBG: docker.version %s" % (info['Components'][0]['Version']))
    except:
      print("FATAL: Docker Not Found")
      sys.exit(1)
    if not 'CONTAINER_NAME' in self.config:
      print("ERR: getDocker: 'CONTAINER_NAME' Not Found (mod='%s')" % self.moduleName)
    else:
      self.containerName = self.config['CONTAINER_NAME']

  def isDocker(self):
    """ Get parameters of module for docker
        Returns
        -------
        ok
            success
    """
    return ('CONTAINER_NAME' in self.config)

  def build(self):
    """ Build docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
        config : dictionary
            configuration of module
    """
    if not self.isDocker():
      print("ERR: Docker build: 'DOCKERFILE' Not Found (mod='%s')" % self.moduleName)
      return False

    fpath = os.path.abspath(self.pathTmp)
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    dockerfile = os.path.join(fpath, self.config['DOCKERFILE'])
    buildpath = os.path.join(fpath, self.config['DOCKER_BUILDPATH'])

    self.stop()
    self.remove()

    try:
      print("LOG: Docker: Build '%s' container..." % self.containerName)
      if self.verbose:
        print("DBG: Docker: Build '%s' container: path=%s" % (self.containerName, buildpath))
        print("DBG: Docker: Build '%s' container: Dockerfile=%s" % (self.containerName, dockerfile))
      image, build_logs = self.docker.images.build(path = buildpath, tag=self.containerName, nocache=True, rm=True, forcerm=True, dockerfile=dockerfile)
      self.config['CONTAINER_SRC'] = self.containerName
      if self.verbose:
        for line in build_logs:
          if 'stream' in line:
            print("DBG: Docker: Build '%s' container: %s" %  (self.containerName, line['stream'].replace("\n", '')))
            
    except Exception as e:
      print("FATAL: Docker build container '%s': %s" % (self.containerName, str(e)))
      return False
    return True

  def status(self):
    """ Status docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker build: 'DOCKERFILE' Not Found (mod='%s')" % self.moduleName)
      return 'not found'

    try:
      print("LOG: Docker: Status '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
    except:
      print("LOG: Docker: Container '%s' Not Found" % (self.containerName))
      return 'not found'
    return container.status

  def start(self):
    """ Start docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker start: Not Found (mod='%s')" % self.moduleName)
      return False

    try:
      print("LOG: Docker: Stop '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      container.start(timeout=120)
    except:
      print("LOG: Docker: Container '%s' Not Found for starting" % (containerName))
      return False
    return self.statusWaiting('running')

  def stop(self):
    """ Stop docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    if not self.isDocker():
      print("ERR: Docker stop: Not Found (mod='%s')" % self.moduleName)
      return False
  
    try:
      print("LOG: Docker: Stop '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      container.stop(timeout=120)
    except:
      print("LOG: Docker: Container '%s' Not Found for stopping" % (self.containerName))
      return False
    return self.statusWaiting('stopped')


  def remove(self):
    """ Remove docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker remove: Not Found (mod='%s')" % self.moduleName)
      return False
  
    try:
      print("LOG: Docker: Remove '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      container.remove(force=True, v=True)
    except:
      print("LOG: Docker: Container '%s' Not Found for removing" % (self.containerName))
      return False
    return True

  def logs(self):
    """ Output logs of docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker logs: Not Found (mod='%s')" % self.moduleName)
      return '', False

    try:
      print("LOG: Docker: Logs '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      return container.logs(), True
    except:
      print("WRN: Docker: Container '%s' Not Found" % (self.containerName))
    return '', False

  def run(self):
    """ Run docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    if not self.isDocker():
      print("ERR: Docker run: Not Found (mod='%s')" % self.moduleName)
      return False
    
    # Parse Ports
    ports = dict()
    if 'CONTAINER_PORTS' in self.config:
      for item in self.config['CONTAINER_PORTS'].split(','):
        it = item.split(':')
        ports[it[1]] = it[0]
    
    # Parse Env
    env_const = 'CONTAINER_ENV_'
    envs = dict()
    for key, value in self.config.items():
      if env_const in key:
        k = key.replace(env_const, '')
        envs[k] = value

    # Parse Volumes
    vol_const = 'CONTAINER_VOL_'
    volumes = dict()
    for key, value in self.config.items():
      if vol_const in key:
        it = value.split(':')
        p = os.path.abspath(it[0])
        if len(it) > 2:
          volumes[p] = {'bind': it[1], 'mode': it[2]}
        else:
          volumes[p] = {'bind': it[1]}

    self.remove()
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    try:
      print("LOG: Docker: Run '%s' container" % self.containerName)
      container = self.docker.containers.run(self.config['CONTAINER_SRC'], name=self.containerName, ports=ports, environment=envs, volumes=volumes, detach=True)
      self.statusWaiting('running')

    except Exception as e:
      print("FATAL: Docker run container '%s': %s" % (self.containerName, str(e)))
      return False
    return True

  def statusWaiting(self, status, timeout = 120):
    """ Waiting docker container status
        Parameters
        ----------
        status : str
            status
        timeout : int
            timeout in seconds
    """
    if not self.isDocker():
      print("ERR: Docker status: Not Found (mod='%s')" % self.moduleName)
      return False
    
    stop_time = 5
    elapsed_time = 0
    container = None
    try:
      container = self.docker.containers.get(self.containerName)
    except:
      if container is None and status == 'not found':
        return True
    while (((container is not None) and container.status != status) or (container is None)) and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      if self.verbose:
        if container is None:
          print("DBG: WAIT: Container '%s': status='%s' != 'not found'=container.status * elapsed_time=%d" % (self.containerName, status, elapsed_time))
        else:
          print("DBG: WAIT: Container '%s': status='%s' != '%s'=container.status * elapsed_time=%d" % (self.containerName, status, container.status, elapsed_time))
      try:
        container = self.docker.containers.get(self.containerName)
      except Exception as e:
        if self.verbose:
          print("ERR: Docker status container '%s': %s" % (self.containerName, str(e)))
      continue
    if container is None:
      return 'not found' == status
    return container.status == status

