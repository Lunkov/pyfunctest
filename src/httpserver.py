#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Class for work with testing Modules '''

import os
import sys
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from .fmod import FMod

class myHTTPServer(SimpleHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    print("LOG: GET request '%s'" % str(self.path))
    self._set_response()
    if str(self.path) == '/liveness':
      self.wfile.write('{"status": "ok"}'.encode('utf8'))
      return
    if str(self.path) == '/readiness':
      self.wfile.write('{"status": "ok"}'.encode('utf8'))
      return


    self.wfile.write('{"status": "not found"}'.encode('utf8'))

  def do_POST(self):
    self.wfile.write('{"status": "not supported"}'.encode('utf8'))
        
class HTTPSrv(FMod):
  ''' Class for work with HTTP (server) '''

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
    super(HTTPSrv, self).__init__(config, pathTmp, verbose)
    
    self.host = 'localhost'
    self.port = '80'
    if 'HTTP_PORT' in self.config:
      self.port = self.config['HTTP_PORT']
    self.port = int(self.port)

    self.url = "http://%s:%d" % (self.host, self.port)
    
    self.server = None
    self.thread = None

  def start(self):
    try:
      self.server = HTTPServer((self.host, self.port), myHTTPServer)
      self.thread = threading.Thread(target = self.server.serve_forever)
      self.thread.deamon = True    
      self.thread.start()
    except Exception as e:
      print("FATAL: HTTP Server '%s' start: %s" % (self.url, str(e)))
      return False

    return True
    
  def stop(self):
    try:
      self.server.shutdown()
    except Exception as e:
      print("FATAL: HTTP Server '%s' stop: %s" % (self.url, str(e)))
      return False
      
    self.server = None
    self.thread = None
    return True
  
  def status(self):
    if self.thread is None:
      return 'stopped'
      
    return 'running'
