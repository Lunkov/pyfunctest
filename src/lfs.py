#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import shutil
from pathlib import Path
if os.name == 'nt':
  import win32api, win32con


class LFS(object):
  ''' Class for load and build environment modules for functional tests '''
  
  @staticmethod 
  def isHidden(f):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(f)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return f.startswith('.') #linux-osx

  @staticmethod 
  def rm(path):
    """ remove folders
    """
    shutil.rmtree(path, ignore_errors=True)
    mypath = Path(path)
    if mypath.is_dir():
      [os.remove(f) for f in os.listdir(path) if file_is_hidden(f)]
