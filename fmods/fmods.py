#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import git
import shutil
import docker
from dotenv import dotenv_values
from pprint import pprint

class FMods(object):
  ''' class for dynamic load modules '''

  def __init__ (self, path_modules, path_tmp, verbose):
    """Initialising object"""
    self.verbose = verbose
    self.path_modules = os.path.abspath(path_modules)
    self.path_tmp = path_tmp
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
    # check subfolders
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
          self.mod_dict[cur_dir] = config
        else:
          if self.verbose:
            print("WRN: Module not found in %s" % full_path)

  def print_list(self):
    for name, _ in self.mod_dict.items():
      print("LOG: mod: %s" % name)

  def get_tmp_folder(self, module_name):
    return os.path.join(os.getcwd(), 'tmp', 'git', module_name)

  def git_clone(module_name, config):
    ''' load module by name '''
    fpath = get_tmp_folder(module_name)
    shutil.rmtree(fpath, ignore_errors=True)
    os.makedirs(fpath, exist_ok=True)
    if self.verbose:
      print("DBG: git.clone.%s: %s => %s" % (module_name, config['GIT_SRC'], fpath))
    repo = git.Repo.clone_from(config['GIT_SRC'], fpath, branch=config['GIT_BRANCH'])
    if not 'CONTAINER_NAME' in config:
      print("ERR: 'CONTAINER_NAME' Not Found (mod='%s')" % module_name)
      return

  def prepare_module(self, module_name, config):
    ''' load module by name '''
    fpath = get_tmp_folder(module_name)
    # HELP: https://docker-py.readthedocs.io/en/stable/containers.html
    dockerfile = os.path.join(fpath, config['DOCKERFILE'])
    buildpath = os.path.join(fpath, config['DOCKER_BUILDPATH'])

    try:
      print("LOG: Docker: Remove '%s' container" % config['CONTAINER_NAME'])
      container = client.containers.get(config['CONTAINER_NAME'])
      container.remove(force=True, v=True)
    except:
      print("LOG: Container '%s' Not Found" % (config['CONTAINER_NAME']))

    try:
      print("LOG: Docker: Build '%s' container: path=%s" % (config['CONTAINER_NAME'], buildpath))
      print("LOG: Docker: Build '%s' container: Dockerfile=%s" % (config['CONTAINER_NAME'], dockerfile))
      client.images.build(path = buildpath, tag=config['CONTAINER_NAME'], nocache=True, rm=True, forcerm=True, dockerfile=dockerfile)
      print("LOG: Docker: Run '%s' container" % config['CONTAINER_NAME'])
      container = client.containers.run(config['CONTAINER_NAME'], name=config['CONTAINER_NAME'], detach=True)
    except Exception as e:
      print("FATAL: Docker build container '%s': %s" % (config['CONTAINER_NAME'], str(e)))
