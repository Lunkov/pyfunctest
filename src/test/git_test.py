#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
from src.fmods import FMods

class TestGIT(unittest.TestCase):

  def testClone(self):
    fm = FMods('data/mods/')
		
    self.assertEqual(fm.count(), 0)
    
    fm.scan()
    self.assertTrue(fm.count() > 7)
   
    # Test: Docker build
    srvGit = fm.newGIT('srv-report')
    
    self.assertTrue(srvGit.clone())
    
    self.assertTrue(os.path.isfile(os.path.join(fm.getTmpFolder('srv-report'), 'README.md')))
    

if __name__ == '__main__':
  unittest.main()
