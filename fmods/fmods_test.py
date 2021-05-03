#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from fmods import FMods

class TestFMods(unittest.TestCase):

  def test_scan(self):
    fm = FMods("./mods/", "./tmp/", True)
		
    self.assertEqual(fm.get_mods_count(), 0)
    self.assertEqual(fm.get_mod_config('pg'), {})
    self.assertEqual(fm.get_tmp_folder('pg'), './tmp/git/pg')
    
    fm.scan()
    self.assertEqual(fm.get_mods_count(), 1)
    config_need = dict(sorted({('NAME', 'pg'), ('GIT_SRC', 'https://github.com/docker-library/postgres.git'), ('GIT_BRANCH', 'master'),('DOCKERFILE','13/Dockerfile'),('DOCKER_BUILDPATH','13/'),('CONTAINER_NAME','pg-test'),('CONTAINER_SRC','postgres:alpine')}))
    self.assertEqual(fm.get_mod_config('pg'), config_need)
    
    dbconn = fm.get_connect_to_postresql('pg')
    self.assertEqual(dbconn, None)
    

if __name__ == '__main__':
  unittest.main()
