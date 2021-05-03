#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name='fmods',
  version='0.0.1',
  packages = find_packages(),
  license="MIT",
  author="Sergey Lunkov",
  install_requires=[
    "gitpython",
    "python-dotenv",
    "docker",
    "psycopg2",
    "shutil",
  ],
)
