#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name='fmods',
  version='0.0.4',
  license="MIT",
  author="Sergey Lunkov",
  package_dir={'fmods': 'src'},
  packages=['fmods'],
  install_requires=[
    "gitpython",
    "python-dotenv",
    "docker",
    "docker-compose",
    "minio",
    "mysqlclient",
    "psycopg2",
    "pika",
    "kafka-python",
  ],
)
