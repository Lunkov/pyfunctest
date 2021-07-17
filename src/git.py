#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import git
from .lfs import LFS
from .fmod import FMod

class GIT(FMod):
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
    super(GIT, self).__init__(config, pathTmp, verbose)
  
  def clone(self):
    """ Clone git repository
    """
    LFS.rm(self.pathTmp)
    if not 'git' in self.config:
      return

    if self.verbose:
      print("DBG: git.Clone(%s): %s => %s" % (self.moduleName, self.config['git']['src'], self.pathTmp))
    repo = git.Repo.clone_from(self.config['git']['src'], self.pathTmp, branch=self.config['git']['branch'])
    return True
