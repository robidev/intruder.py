#!/usr/bin/python3
import os
import subprocess

#list files in init subdir
initpath = "./init/"

#call subprocess.Popen() on each file
for _,_,files in os.walk(initpath):
  for f in files:
    subprocess.Popen(initpath + f)

#call sshd -D as the final process
if os.path.exists('/usr/sbin/sshd'):
  os.execv('/usr/sbin/sshd',['-D'])