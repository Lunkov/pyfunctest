#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
from src.fmods import FMods
from src.git import GIT

class TestGIT(unittest.TestCase):

  def testClone(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertEqual(fm.count(), 5)
   
    # Test: Docker build
    srvGit = GIT(fm.getConfig('srv-report'), fm.getTmpFolder('srv-report'), True)
    
    ok = srvGit.clone()
    self.assertEqual(ok, True)
    
    self.assertEqual(os.path.isfile(os.path.join(fm.getTmpFolder('srv-report'), 'README.md')), True)
    

if __name__ == '__main__':
  unittest.main()
