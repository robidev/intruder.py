import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 10514
host='gamemaster'
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
  try:
    data, addr = sock.recvfrom(65356) # buffer size is 65k bytes
    if data:
      sock.sendto(data,(host,UDP_PORT))
  except socket.error as msg:
    pass