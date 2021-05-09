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

  def gitClone(self, moduleName):
    """ Clone git repository of module
        Parameters
        ----------
        moduleName : str
            name of module
        config : dictionary
            configuration of module
    """
    config = self.getConfig(moduleName)
    if not 'GIT_SRC' in config:
      print("LOG: 'GIT_SRC' Not Found (mod='%s')" % moduleName)
      return False
    fpath = self.getTmpFolder(moduleName)
    shutil.rmtree(fpath, ignore_errors=True)
    os.makedirs(fpath, exist_ok=True)
    if self.verbose:
      print("DBG: git.clone.%s: %s => %s" % (moduleName, config['GIT_SRC'], fpath))
    repo = git.Repo.clone_from(config['GIT_SRC'], fpath, branch=config['GIT_BRANCH'])
    return True

  def getDocker(self, moduleName):
    """ Get parameters of module for docker
        Parameters
        ----------
        moduleName : str
            name of module
        Returns
        -------
        containerName
            a name of docker container
        config
            a dictionary of strings
        ok
            success
    """
    config = self.getConfig(moduleName)
    if not 'CONTAINER_NAME' in config:
      print("ERR: getDocker: 'CONTAINER_NAME' Not Found (mod='%s')" % moduleName)
      print(traceback.format_exc())
      return '', config, False
    return config['CONTAINER_NAME'], config, True

  def dockerBuild(self, moduleName):
    """ Build docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
        config : dictionary
            configuration of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False
    if not 'DOCKERFILE' in config:
      print("ERR: Docker build: 'DOCKERFILE' Not Found (mod='%s')" % moduleName)
      return False

    fpath = os.path.abspath(self.getTmpFolder(moduleName))
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    dockerfile = os.path.join(fpath, config['DOCKERFILE'])
    buildpath = os.path.join(fpath, config['DOCKER_BUILDPATH'])

    self.dockerStop(containerName)
    self.dockerRemove(containerName)

    try:
      print("LOG: Docker: Build '%s' container..." % containerName)
      if self.verbose:
        print("DBG: Docker: Build '%s' container: path=%s" % (containerName, buildpath))
        print("DBG: Docker: Build '%s' container: Dockerfile=%s" % (containerName, dockerfile))
      image, build_logs = self.docker.images.build(path = buildpath, tag=containerName, nocache=True, rm=True, forcerm=True, dockerfile=dockerfile)

      if self.verbose:
        for line in build_logs:
          if 'stream' in line:
            print("DBG: Docker: Build '%s' container: %s" %  (containerName, line['stream'].replace("\n", '')))
            
    except Exception as e:
      print("FATAL: Docker build container '%s': %s" % (containerName, str(e)))
      return False
    return True

  def dockerStatus(self, moduleName):
    """ Status docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return 'not found'
    try:
      print("LOG: Docker: Status '%s' container" % containerName)
      container = self.docker.containers.get(containerName)
    except:
      print("LOG: Docker: Container '%s' Not Found" % (containerName))
      return 'not found'
    return container.status

  def dockerStart(self, moduleName):
    """ Start docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False
    try:
      print("LOG: Docker: Stop '%s' container" % containerName)
      container = self.docker.containers.get(containerName)
      container.start(timeout=120)
    except:
      print("LOG: Docker: Container '%s' Not Found for starting" % (containerName))
      return False
    return self.dockerStatusWaiting(moduleName, 'running')

  def dockerStop(self, moduleName):
    """ Stop docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False
  
    try:
      print("LOG: Docker: Stop '%s' container" % containerName)
      container = self.docker.containers.get(containerName)
      container.stop(timeout=120)
    except:
      print("LOG: Docker: Container '%s' Not Found for stopping" % (containerName))
      return False
    return self.dockerStatusWaiting(moduleName, 'stopped')


  def dockerRemove(self, moduleName):
    """ Remove docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False
  
    try:
      print("LOG: Docker: Remove '%s' container" % containerName)
      container = self.docker.containers.get(containerName)
      container.remove(force=True, v=True)
      return self.dockerStatus(moduleName) == 'not found'
    except:
      print("LOG: Docker: Container '%s' Not Found for removing" % (containerName))
      return False
    return True

  def dockerLogs(self, moduleName):
    """ Output logs of docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return '', False

    try:
      print("LOG: Docker: Logs '%s' container" % containerName)
      container = self.docker.containers.get(containerName)
      return container.logs(), True
    except:
      print("WRN: Docker: Container '%s' Not Found" % (containerName))
    return '', False

  def dockerRun(self, moduleName):
    """ Run docker container of module
        Parameters
        ----------
        moduleName : str
            name of module
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False
    
    # Parse Ports
    ports = dict()
    if 'CONTAINER_PORTS' in config:
      for item in config['CONTAINER_PORTS'].split(','):
        it = item.split(':')
        ports[it[1]] = it[0]
    
    # Parse Env
    env_const = 'CONTAINER_ENV_'
    envs = dict()
    for key, value in config.items():
      if env_const in key:
        k = key.replace(env_const, '')
        envs[k] = value

    # Parse Volumes
    vol_const = 'CONTAINER_VOL_'
    volumes = dict()
    for key, value in config.items():
      if vol_const in key:
        it = value.split(':')
        p = os.path.abspath(it[0])
        if len(it) > 2:
          volumes[p] = {'bind': it[1], 'mode': it[2]}
        else:
          volumes[p] = {'bind': it[1]}

    fpath = self.getTmpFolder(moduleName)
    self.dockerRemove(moduleName)
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    try:
      print("LOG: Docker: Run '%s' container" % containerName)
      container = self.docker.containers.run(config['CONTAINER_SRC'], name=containerName, ports=ports, environment=envs, volumes=volumes, detach=True)
      self.dockerStatusWaiting(moduleName, 'running')

    except Exception as e:
      print("FATAL: Docker run container '%s': %s" % (containerName, str(e)))
      return False
    return True

  def dockerStatusWaiting(self, moduleName, status, timeout = 120):
    """ Waiting docker container status
        Parameters
        ----------
        moduleName : str
            name of module
        status : str
            status
        timeout : int
            timeout in seconds
    """
    containerName, config, ok = self.getDocker(moduleName)
    if not ok:
      return False

    stop_time = 5
    elapsed_time = 0
    container = self.docker.containers.get(containerName)
    while container.status != status and elapsed_time < timeout:
      time.sleep(stop_time)
      elapsed_time += stop_time
      if self.verbose:
        print("DBG: WAIT: status='%s' '%s'=container.status * elapsed_time=%d" % (status, container.status, elapsed_time))
      container = self.docker.containers.get(containerName)
      continue
    return container.status == status

  def getConnectToPostreSQL(self, moduleName):
    """ Connect to postgresql database
        Attributes
        ----------
        moduleName : str
            name of module
    """
    config = self.getConfig(moduleName)
    if not 'DB_NAME' in config:
      print("LOG: SQL: Module '%s'. DB_NAME Not Found" % (moduleName))
      return None
    if not 'DB_USER' in config:
      print("LOG: SQL: Module '%s'. DB_USER Not Found" % (moduleName))
      return None
    if not 'DB_PASSWORD' in config:
      print("LOG: SQL: Module '%s'. DB_PASSWORD Not Found" % (moduleName))
      return None

    host = 'localhost'
    if 'DB_HOST' in config:
      host = config['DB_HOST']
    port = '5432'
    if 'DB_PORT' in config:
      port = config['DB_PORT']

    try:
      handle = psycopg2.connect(host=host,
                            port=port,
                            user=config['DB_USER'],
                            password=config['DB_PASSWORD'],
                            dbname=config['DB_NAME'])
      return handle
    except Exception as e:
      print("FATAL: Connect to DB '%s': %s" % (config['CONTAINER_NAME'], str(e)))
    return None

  def startAll(self):
    """ setUp for UTests
    """
    for moduleName, config in self.modules.items():
      if 'GIT_SRC' in config:
        self.git_clone(moduleName)
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
