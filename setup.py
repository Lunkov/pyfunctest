#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name='pyfunctest',
  version='0.0.5',
  license="MIT",
  author="Sergey Lunkov",
  package_dir={'pyfunctest': 'src'},
  packages=['pyfunctest'],
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
