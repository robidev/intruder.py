import psutil
import socket
import json
import time
from subprocess import PIPE

h='gamemaster'
#h='127.0.0.1'
#h='192.168.192.21'

p=10514
hs=socket.gethostname()
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(str.encode(json.dumps({'event':'log_event', 'data':{'host':hs,'data':'','clear':1}})),(h,p))
fi=open("/tmp/tst","w+")
fi.write("[+] logging started\n")
fi.close()
logfile=open("/tmp/tst",'r')

try:
  fi = open('/usr/sbin/sshd')
  fi.close()
  fi= open("/tmp/tst","a")
  fi.write("[+] sshd found")
  psutil.Popen(["/usr/sbin/sshd"])
  fi.write("[+] sshd started")
  fi.close()
except FileNotFoundError:
  fi= open("/tmp/tst","a")
  fi.write('[-] no sshd found')
  fi.close()


line=''
while True:
  
  e = time.strftime("last updated:\t%d %b %Y %H:%M:%S\n---\nuser\tPID\tname\tCMD\n", time.gmtime())
  for proc in psutil.process_iter(attrs=['username','pid','name','cmdline']):
    d="%s\t%s\t%s\t%s\n"%(proc.info['username'],proc.info['pid'],proc.info['name'],proc.info['cmdline'])
    e+=d
  f={'event':'info_event', 'data':{'host':hs,'type':'0','data':e}}
  s.sendto(str.encode(json.dumps(f)),(h,p))

  #info syslog
  pr = psutil.Popen(["/usr/bin/tail", "/var/log/syslog"], stdout=PIPE)
  pr.wait(timeout=2)
  d1,d3=pr.communicate()
  d= d1.decode('utf-8')
  f={'event':'info_event', 'data':{'host':hs,'type':'1','data':d}}
  s.sendto(str.encode(json.dumps(f)),(h,p))

  #info net
  e=""
  a=psutil.net_connections()
  for b in a:
    e+= "%s %s %s\n" % (b.laddr, b.raddr, b.status)
  f={'event':'info_event', 'data':{'host':hs,'type':'2','data':e}}
  s.sendto(str.encode(json.dumps(f)),(h,p))
  
  #info ifconfig
  e=""
  t=psutil.net_if_stats()
  a=psutil.net_if_addrs()
  for b,c in a.items():
    if b == 'lo':
      continue
    if b in t:
      e+= "if=%s ip=%s subnet=%s status=%s\n" % (b,c[0].address,c[0].netmask,t[b].isup)
  f={'event':'info_event', 'data':{'host':hs,'type':'3','data':e}}
  s.sendto(str.encode(json.dumps(f)),(h,p))

  #forward all log-lines
  tmp = logfile.readline()
  if tmp is not None:
    line += tmp
    if line.endswith("\n"):
      e={'event':'log_event', 'data':{'host':hs,'data':line,'clear':0}}
      s.sendto(str.encode(json.dumps(e)),(h,p))
      line = ''
  
  time.sleep(1)
  fi= open("/tmp/tst","a")
  fi.write("%s:tick\n" % hs)
  fi.close()
