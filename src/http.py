#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import requests
from requests.exceptions import HTTPError

class HTTP():
  ''' Class for work with HTTP (client) '''

  def __init__ (self, config, pathTmp, verbose):
    """ Initialising object
    Parameters
    ----------
    config : dict
        config of module
    pathTmp : str
        path to temporary files
    verbose : bool
        verbose output
    """
    self.verbose = verbose
    self.config = config
    self.pathTmp = pathTmp
    self.moduleName = self.config['NAME']
    self.host = 'localhost'
    if 'HTTP_HOST' in self.config:
      self.host = self.config['HTTP_HOST']
    self.port = '21'
    if 'HTTP_PORT' in self.config:
      self.port = self.config['HTTP_PORT']
    self.port = int(self.port)

    self.url = "http://%s:%d" % (self.host, self.port)

  def get(self, url):
    rUrl = "%s/%s" % (self.url, url)
    try:
      if self.verbose:
        print("DBG: HTTP GET '%s'" % (rUrl))
      response = requests.get(rUrl)
       # если ответ успешен, исключения задействованы не будут
      response.raise_for_status()
    except HTTPError as http_err:
      print("FATAL: HTTP(%s) error occurred: %s" % (rUrl, http_err))
      return None, False
    except Exception as err:
      print("FATAL: HTTP(%s) other error occurred: %s" % (rUrl, err))
      return None, False

    if self.verbose:
      print("DBG: HTTP GET '%s': status code=%d" % (rUrl, response.status_code))
    return response, True

  def getStatusLiveness(self):
    response, ok = self.get('liveness')
    if not ok:
      return 'HTTP: 404 Not Found', False
    a = []
    try:
      a = response.json()
    except Exception as err:
      print("FATAL: JSON Parse Error '%s': %s" % (response.content, str(err)))
      return 'HTTP: JSON Parse Error', False
          
    if 'error' in a:
      return a['error'], False
    if 'status' in a:
      return a['status'], a['status'] == 'ok'
    
    return 'HTTP: Status not found', False

  def getStatusReadiness(self):
    response, ok = self.get('readiness')
    if not ok:
      return 'HTTP: 404 Not Found', False

    a = []
    try:
      a = response.json()
    except Exception as err:
      print("FATAL: JSON Parse Error '%s': %s" % (response.content, str(err)))
      return 'HTTP: JSON Parse Error', False

    if 'error' in a:
      return a['error'], False
    if 'status' in a:
      return a['status'], a['status'] == 'ok'
    
    return 'HTTP: Status not found', False
