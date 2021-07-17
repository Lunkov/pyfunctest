#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

class FMod():
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
    self.verbose = verbose
    self.config = config
    self.pathTmp = pathTmp
    self.moduleName = 'undefined'
    if 'name' in self.config:
      self.moduleName = self.config['name']
      
    self.handle = None
    self.host = '127.0.0.1'
    self.port = 0
    self.user = ''
    self.password = ''


  def isDocker(self):
    """ Get parameters of module for docker
        Returns
        -------
        ok
            success
    """
    if 'docker' in self.config:
      if 'name' in self.config['docker']:
        return True
    return False

  def close(self):
    if not self.handle is None:
      if hasattr(self.handle, 'close') and callable(getattr(self.handle, 'close')):
        self.handle.close()
    self.handle = None

  def getHandle(self):
    return self.handle
