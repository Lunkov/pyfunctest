#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import io
import sys
import time
import subprocess
import docker
import tarfile

from .fmod import FMod

class Docker(FMod):
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
    super(Docker, self).__init__(config, pathTmp, verbose)
    
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
      print("ERR: Docker(%s) network(%s) Not Found" % (self.moduleName, self.networkName))
    if net is None:
      self.docker.networks.create(self.networkName, driver="bridge")
    
    if 'docker' in self.config:
      if 'name' in self.config['docker']:
        self.containerName = self.config['docker']['name']
      else:
        print("ERR: getDocker: 'docker:name' Not Found (mod='%s')" % self.moduleName)

  def build(self, rm=True):
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
    dockerfile = os.path.join(fpath, self.config['docker']['dockerfile'])
    buildpath = fpath
    if 'buildpath' in self.config['docker']:
      buildpath = os.path.join(fpath, self.config['docker']['buildpath'])

    if rm:
      self.stop()
      self.remove()

    try:
      print("LOG: Docker: Build '%s' container..." % self.containerName)
      if self.verbose:
        print("DBG: Docker: Build '%s' container: path=%s" % (self.containerName, buildpath))
        print("DBG: Docker: Build '%s' container: Dockerfile=%s" % (self.containerName, dockerfile))
      image, build_logs = self.docker.images.build(path = buildpath, tag=self.containerName, nocache=True, rm=True, forcerm=True, dockerfile=dockerfile)
      self.config['docker']['src'] = self.containerName
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
      print("LOG: Docker: Start '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      container.start(timeout=120)
    except:
      print("LOG: Docker: Container '%s' Not Found for starting" % (containerName))
      return False
    return self.statusWaiting('running')

  def restart(self):
    """ Start docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker restart: Not Found (mod='%s')" % self.moduleName)
      return False

    try:
      if self.verbose:
        print("DBG: Docker: Restart '%s' container" % self.containerName)
      container = self.docker.containers.get(self.containerName)
      container.restart()
    except:
      print("LOG: Docker: Container '%s' Not Found for restarting" % (self.containerName))
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

  def run(self, rm = True):
    """ Run docker container of module
    """
    if not self.isDocker():
      print("ERR: Docker run: Not Found (mod='%s')" % self.moduleName)
      return False
    
    command = None
    if 'run_command' in self.config['docker']:
      command = self.config['docker']['run_command']
    
    # Parse Ports
    ports = dict()
    if 'ports' in self.config['docker']:
      for item in self.config['docker']['ports']:
        try:
          it = item.split(':')
          if len(it) == 2:
            ip = it[1].split('-')
            if len(ip) == 1:
              ports[it[1]] = it[0]
            else:
              # Range of ports. Example: 1000-1010:2000-2010
              p = 0
              ip2 = it[0].split('-')
              for i in range(int(ip[0]), int(ip[1])):
                ports[i] = int(ip2[0]) + p
                p += 1
          else:
            print("WRN: Docker: Container '%s': Bad ports '%s'" % (self.containerName, item))
        except Exception as e:
          print("ERR: Docker: Container '%s': %s" % (self.containerName, str(e)))

    # Parse Env
    envs = dict()
    if 'env' in self.config['docker']:
      for item in self.config['docker']['env']:
        for key, value in item.items():
          envs[key] = value

    # Parse Volumes
    volumes = dict()
    if 'volumes' in self.config['docker']:
      for item in self.config['docker']['volumes']:
        if type(item) != 'dict':
          print("WRN: Docker: Container '%s': Bad volumes '%s'" % (self.containerName, item))
          continue
        for key, value in item.items():
          envs[key] = value
          it = value.split(':')
          p = os.path.abspath(it[0])
          if len(it) > 2:
            volumes[p] = {'bind': it[1], 'mode': it[2]}
          else:
            volumes[p] = {'bind': it[1]}

    if rm:
      self.remove()
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    try:
      print("LOG: Docker: Run '%s' container" % self.containerName)
      container = self.docker.containers.run(self.config['docker']['src'], command=command, network=self.networkName, name=self.containerName, domainname=self.containerName, hostname=self.containerName, ports=ports, environment=envs, volumes=volumes, detach=True)
      self.statusWaiting('running')

    except Exception as e:
      print("FATAL: Docker run container '%s': %s" % (self.containerName, str(e)))
      return False
      
    if 'patch' in self.config['docker']:
      for item in self.config['docker']['patch']:
        for path_src, path_dst in item.items():
          srcPath = os.path.join(self.config['mod_path'] , path_src)
          self.copy(srcPath, path_dst)
      self.restart()

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

  def getNameDockerCompose(self, fileName = ''):
    if len(fileName) < 1:
      dcf = 'docker-compose.yml'
      if 'compose' in self.config['docker']:
        dcf = self.config['docker']['compose']
      fileName = os.path.join(self.config['mod_path'], dcf)
    return fileName
    
  def runProcess(self, action, cmd, fileName):
    try:
      if self.verbose:
        print("DBG: %sing Docker-Compose '%s'" % (action, fileName))
      popen = subprocess.Popen(cmd, shell=True, universal_newlines=True)

      output, error = popen.communicate(timeout=60)
      if self.verbose:
        print("DBG: %sed Docker-Compose '%s'" % (action, fileName))
    except subprocess.CalledProcessError as e:
      print("FATAL: %s Docker-Compose '%s': %s" % (action, fileName, e.output))
      return False
    except Exception as e:
      print("FATAL: %s Docker-Compose '%s': %s" % (action, fileName, str(e)))
      return False
    return popen.returncode == 0

  def startCompose(self, fileName = ''):
    fileName = self.getNameDockerCompose(fileName)
    return self.runProcess("Start", "docker-compose --file %s up --force-recreate --detach" % fileName, fileName)

  def stopCompose(self, fileName = ''):
    fileName = self.getNameDockerCompose(fileName)
    return self.runProcess("Stop", "docker-compose --file %s down" % fileName, fileName) # --rmi all

  def copy(self, src, dstDir):
    """ src shall be an absolute path """
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w|') as tar, open(src, 'rb') as f:
      info = tar.gettarinfo(fileobj=f)
      info.name = os.path.basename(src)
      tar.addfile(info, f)

    try:
      container = self.docker.containers.get(self.containerName)
      container.put_archive(dstDir, stream.getvalue())
    except Exception as e:
      print("FATAL: Docker copy container '%s': %s" % (self.containerName, str(e)))
      return False

    return True
