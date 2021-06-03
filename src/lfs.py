#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import glob
import shutil
import stat
from pathlib import Path

class LFS(object):
  ''' Class for load and build environment modules for functional tests '''

  @staticmethod
  def rm(pathName):
    """ remove folders
    """
    shutil.rmtree(pathName, ignore_errors=True)
    mypath = Path(pathName)
    if mypath.is_dir():
      for root, dirs, files in os.walk(pathName):
        for f in files:
          try:
            os.chmod(os.path.join(root, f),stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH|stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR|stat.S_IWGRP|stat.S_IXGRP)
          except:
            continue
          os.remove(os.path.join(root, f))
        for d in dirs:
          shutil.rmtree(os.path.join(root, d), ignore_errors=True)
      for f in os.scandir(pathName):
        try:
          if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
          if f.is_file():
            os.remove(f)
        except:
          continue
