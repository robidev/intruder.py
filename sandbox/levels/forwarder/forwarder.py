import socket
import time

logfilename = "/tmp/tst"

def logline(text):
  logfile=open(logfilename,'a')
  logfile.write(text + "\n")
  logfile.close()

UDP_IP = "0.0.0.0"
UDP_PORT = 10514
REFRESH_HOSTS_PORT = 10516

host='gamemaster'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setblocking(False)
sock.bind((UDP_IP, UDP_PORT))

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock2.setblocking(False)
sock2.bind((UDP_IP, REFRESH_HOSTS_PORT))

refresh_log = {}
logline("forwarder started")
while True:
  try:
    data, (ip, port) = sock.recvfrom(65356) # buffer size is 65k bytes
    if data:
      if ip not in refresh_log:
        refresh_log[ip] = ip
      sock.sendto(data,(host,UDP_PORT))
  except socket.error as msg:
    pass

  try:
    data2, (_, _) = sock2.recvfrom(1024) # buffer size is 1k
    if data2: 
      if data2 == b"reset_log\n":
        logline("reset")
        for addr in refresh_log:
          logline(addr)
          sock.sendto(b"reset_log\n",(addr,REFRESH_HOSTS_PORT))
  except socket.error as msg:
    pass  

  time.sleep(0.001)