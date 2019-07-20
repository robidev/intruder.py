#!/usr/local/bin/python3
import psutil
import socket
import json
import time
import sys
import os
from subprocess import PIPE

logfilename = "/tmp/tst"
max_lines = 10

def logline(text):
  logfile=open(logfilename,'a')
  logfile.write(text)
  logfile.close()

master = 'forwarder'
if len(sys.argv) > 1:
  master = sys.argv[1]
master_ip = socket.gethostbyname(master)

port = 10514
if len(sys.argv) >2:
  port = int(sys.argv[2])

logline("[+] logging started\n")

port2 = 10516
host = socket.gethostname()
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#listner
sock.setblocking(False)
sock.bind(('0.0.0.0', port2))

#clear the log buffer
sock.sendto(str.encode(json.dumps({'event':'log_event', 'data':{'host':host,'data':'','clear':1}})),(master,port))

logfile=open("/tmp/tst",'r')
line=''
while True:
  #info ps
  data = time.strftime("last updated:\t%d %b %Y %H:%M:%S\n---\nuser\tPID\tname\tCMD\n", time.gmtime())
  for proc in psutil.process_iter(attrs=['username','pid','name','cmdline']):
    ps_line = "%s\t%s\t%s\t%s\n"%(proc.info['username'],proc.info['pid'],proc.info['name'],proc.info['cmdline'])
    data += ps_line
  sock.sendto(str.encode(json.dumps({'event':'info_event', 'data':{'host':host,'type':'0','data':data}})),(master,port))

  #info syslog
  process = psutil.Popen(["/usr/bin/tail", "/var/log/syslog"], stdout=PIPE)
  process.wait(timeout=2)
  data_bytes,_ = process.communicate()
  data = data_bytes.decode('utf-8')
  sock.sendto(str.encode(json.dumps({'event':'info_event', 'data':{'host':host,'type':'1','data':data}})),(master,port))

  #info net
  data = ""
  connections=psutil.net_connections()
  for conn in connections:
    data += "%s %s %s\n" % (conn.laddr, conn.raddr, conn.status)
  sock.sendto(str.encode(json.dumps({'event':'info_event', 'data':{'host':host,'type':'2','data':data}})),(master,port))
  
  #info ifconfig
  data = ""
  stats = psutil.net_if_stats()
  addrs = psutil.net_if_addrs()
  for eth,ip in addrs.items():
    if eth == 'lo':
      continue
    if eth in stats:
      data += "if=%s ip=%s subnet=%s status=%s\n" % (eth, ip[0].address, ip[0].netmask, stats[eth].isup)
  sock.sendto(str.encode(json.dumps({'event':'info_event', 'data':{'host':host,'type':'3','data':data}})),(master,port))

  #check for retransmitting loglines
  try:
    data, addr = sock.recvfrom(1024) # buffer size is 1k bytes
    if data and data == b'reset_log\n': #and addr == master_ip
      #tail the logfile
      print("reset log")
      logline("[+] reset log\n")

      lines = 0
      logfile.seek(0, os.SEEK_END) #seek end
      position = logfile.tell()
      while position > 0:
        logfile.seek(position)
        next_char = logfile.read(1)
        if next_char == "\n":
          lines += 1
          if lines > max_lines:
            break;
        position -= 1
      logfile.seek(position)
      sock.sendto(str.encode(json.dumps({'event':'log_event', 'data':{'host':host,'data':'','clear':1}})),(master,port))
  except socket.error as msg:
    pass

  #forward all log-lines
  tmp = logfile.readline()
  while tmp is not None and tmp is not "":
    line += tmp
    if line.endswith("\n"):
      sock.sendto(str.encode(json.dumps({'event':'log_event', 'data':{'host':host,'data':line,'clear':0}})),(master,port))
      line = ''
    tmp = logfile.readline()
  
  time.sleep(1)
