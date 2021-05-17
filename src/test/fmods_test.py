#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
from src.fmods import FMods

class TestFMods(unittest.TestCase):

  def testFModsSimple(self):
    fm = FMods("data/mods/", "data/tmp/", True)
		
    self.assertEqual(fm.count(), 0)
    self.assertEqual(fm.getConfig('pg'), {})
    self.assertEqual(fm.getTmpFolder('pg'), 'data/tmp/git/pg')
    
    fm.scan()
    self.assertTrue(fm.count() > 7)

if __name__ == '__main__':
  unittest.main()
