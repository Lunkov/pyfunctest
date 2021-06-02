#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import git
from .lfs import LFS

class GIT(object):
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
    self.moduleName = self.config['NAME']
  
  def clone(self):
    """ Clone git repository
    """
    LFS.rm(self.pathTmp)
    if self.verbose:
      print("DBG: git.Clone(%s): %s => %s" % (self.moduleName, self.config['GIT_SRC'], self.pathTmp))
    repo = git.Repo.clone_from(self.config['GIT_SRC'], self.pathTmp, branch=self.config['GIT_BRANCH'])
    return True
