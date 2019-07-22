#!/usr/local/bin/python3
import sys
import os
import subprocess

proc = '/usr/sbin/sshd' 
arg = '-D' # call sshd -D as the final process
if len(sys.argv) > 1:
  proc = sys.argv[1]
  arg = ''

if len(sys.argv) > 2:
  arg = sys.argv[2]

#list files in init.d subdir
initpath = "init.d/"

#call subprocess.Popen() on each file
for _,_,files in os.walk(initpath):
  for f in files:
    subprocess.Popen(initpath + f)

#call the final process, and wait for it to end
if os.path.exists(proc):
  pid = subprocess.Popen([proc,arg])
  pid.wait() # make init killable by docker, taking all subprocesses with it