#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name='pyfunctest',
  version='0.0.5',
  license="MIT",
  author="Sergey Lunkov",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Lunkov/pyfunctest",
  project_urls={
    "Bug Tracker": "https://github.com/Lunkov/pyfunctest/issues",
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],  
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
