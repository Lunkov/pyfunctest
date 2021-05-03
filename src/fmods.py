#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import git
import shutil
import docker
import psycopg2
from dotenv import dotenv_values
from pprint import pprint

class FMods(object):
  ''' Class for load and build environment modules for functional tests '''

  def __init__ (self, path_modules, path_tmp, verbose):
    """ Initialising object
    Parameters
    ----------
    path_modules : str
        path to modules settings
    path_tmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.path_modules = os.path.abspath(path_modules)
    self.path_tmp = path_tmp
    if self.path_tmp == "":
      self.path_tmp = os.path.join(os.getcwd(), 'tmp')
    self.mod_dict = dict()
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
      print("DBG: scan folder: %s" % self.path_modules)
    lst_dir = os.listdir(self.path_modules)
    for cur_dir in lst_dir:
      if self.verbose:
        print("DBG: scan subfolder: %s" % cur_dir)
      full_path = os.path.join(self.path_modules, cur_dir)
      if os.path.isdir(full_path):
        config = dotenv_values(os.path.join(full_path, ".env"))
        if "NAME" in config:
          if self.verbose:
            print("DBG: find mod: %s" % config['NAME'])
          self.mod_dict[cur_dir] = set()
          self.mod_dict[cur_dir] = dict(sorted(config.items()))
        else:
          if self.verbose:
            print("WRN: Module not found in %s" % full_path)

  def print_list(self):
    """ Output the list of modules
    """
    for name, _ in self.mod_dict.items():
      print("LOG: mod: %s" % name)

  def get_mods_count(self):
    """ Count of modules
    """
    return len(self.mod_dict)

  def get_mod_config(self, module_name):
    """ Get configuration of module
        Parameters
        ----------
        module_name : str
            name of module
    """
    return self.mod_dict.get(module_name, {})

  def get_tmp_folder(self, module_name):
    """ Get temporary path for module
        Parameters
        ----------
        module_name : str
            name of the module
            
        Returns
        -------
        path:
            temporary path for the module
    """
    return os.path.join(self.path_tmp, 'git', module_name)

  def git_clone(module_name, config):
    """ Clone git repository of module
        Parameters
        ----------
        module_name : str
            name of module
        config : dictionary
            configuration of module
    """
    if not 'GIT_SRC' in config:
      print("LOG: 'GIT_SRC' Not Found (mod='%s')" % module_name)
      return
    fpath = get_tmp_folder(module_name)
    shutil.rmtree(fpath, ignore_errors=True)
    os.makedirs(fpath, exist_ok=True)
    if self.verbose:
      print("DBG: git.clone.%s: %s => %s" % (module_name, config['GIT_SRC'], fpath))
    repo = git.Repo.clone_from(config['GIT_SRC'], fpath, branch=config['GIT_BRANCH'])

  def docker_build(self, module_name, config):
    """ Build docker container of module
        Parameters
        ----------
        module_name : str
            name of module
        config : dictionary
            configuration of module
    """
    if not 'CONTAINER_NAME' in config:
      print("ERR: 'CONTAINER_NAME' Not Found (mod='%s')" % module_name)
      return
    if not 'DOCKERFILE' in config:
      print("ERR: Docker build: 'DOCKERFILE' Not Found (mod='%s')" % module_name)
      return

    fpath = get_tmp_folder(module_name)
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    dockerfile = os.path.join(fpath, config['DOCKERFILE'])
    buildpath = os.path.join(fpath, config['DOCKER_BUILDPATH'])

    self.docker_remove(config['CONTAINER_NAME'])

    try:
      print("LOG: Docker: Build '%s' container" % config['CONTAINER_NAME'])
      if self.verbose:
        print("DBG: Docker: Build '%s' container: path=%s" % (config['CONTAINER_NAME'], buildpath))
        print("DBG: Docker: Build '%s' container: Dockerfile=%s" % (config['CONTAINER_NAME'], dockerfile))
      client.images.build(path = buildpath, tag=config['CONTAINER_NAME'], nocache=True, rm=True, forcerm=True, dockerfile=dockerfile)
      print("LOG: Docker: Run '%s' container" % config['CONTAINER_NAME'])
      container = client.containers.run(config['CONTAINER_NAME'], name=config['CONTAINER_NAME'], detach=True)
    except Exception as e:
      print("FATAL: Docker build container '%s': %s" % (config['CONTAINER_NAME'], str(e)))

  def docker_remove(self, container_name):
    """ Remove docker container of module
        Parameters
        ----------
        module_name : str
            name of module
        config : dictionary
            configuration of module
    """
    try:
      print("LOG: Docker: Remove '%s' container" % container_name)
      container = client.containers.get(container_name)
      container.remove(force=True, v=True)
    except:
      print("LOG: Container '%s' Not Found" % (container_name))

  def docker_run(self, module_name, config):
    """ Run docker container of module
        Parameters
        ----------
        module_name : str
            name of module
        config : dictionary
            configuration of module
    """
    if not 'CONTAINER_SRC' in config:
      print("ERR: Docker Run: 'CONTAINER_SRC' Not Found (mod='%s')" % module_name)
      return
    
    fpath = get_tmp_folder(module_name)
    self.docker_remove(config['CONTAINER_NAME'])
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    try:
      print("LOG: Docker: Run '%s' container" % config['CONTAINER_NAME'])
      container = client.containers.run(config['CONTAINER_SRC'], name=config['CONTAINER_NAME'], detach=True)
    except Exception as e:
      print("FATAL: Docker build container '%s': %s" % (config['CONTAINER_NAME'], str(e)))


  def get_connect_to_postresql(self, module_name):
    """ Connect to postgresql database
        Attributes
        ----------
        module_name : str
            name of module
    """
    cfg = self.get_mod_config(module_name)
    if not 'DB_NAME' in cfg:
      print("LOG: SQL: Module '%s'. DB_NAME Not Found" % (module_name))
      return None
    if not 'DB_USER' in cfg:
      print("LOG: SQL: Module '%s'. DB_USER Not Found" % (module_name))
      return None
    if not 'DB_PWD' in cfg:
      print("LOG: SQL: Module '%s'. DB_PWD Not Found" % (module_name))
      return None

    host = 'localhost'
    if 'DB_HOST' in cfg:
      host = cfg['DB_HOST']
    port = '5432'
    if 'DB_PORT' in cfg:
      port = cfg['DB_PORT']

    return psycopg2.connect(host=host,
                            port=port,
                            user=cfg['DB_USER'],
                            password=cfg['DB_PWD'],
                            dbname=cfg['DB_NAME'])

  def setUp(self):
    """ setUp for UTests
    """
    for module_name, config in self.mod_dict.items():
      if 'GIT_SRC' in config:
        self.git_clone(module_name, config)
      self.docker_remove(module_name)
      if 'DOCKERFILE' in config:
        self.docker_build(module_name, config)
      else:
        if 'CONTAINER_SRC' in config:
          self.docker_run(module_name, config)


  def tearDown(self):
    """ tearDown for UTests
    """
    shutil.rmtree(self.path_tmp, ignore_errors=True)
    for module_name, config in self.mod_dict.items():
      self.docker_remove(module_name)
