#!/usr/bin/env python3
import socket
import json
fi=open("/tmp/tst","a")
fi.write("[+] payload executed\n")

h='forwarder'
p=10514
hs=socket.gethostname()
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
fi.write("[+] sending intruder event\n")
s.sendto(str.encode(json.dumps({'event':'intruder_event', 'data':{'host':hs}})),(h,p))

fi.write("[+] sending connect event\n")
s.sendto(str.encode(json.dumps({'event':'connect_event', 'data':{'host':hs,'dest':'sheep2'}})),(h,p))
s.sendto(str.encode(json.dumps({'event':'connect_event', 'data':{'host':'sheep3','dest':'sheep2'}})),(h,p))

s.sendto(str.encode(json.dumps({'event':'flag_event', 'data':{'host':'sheep3','flag':'0123456789'}})),(h,p))

fi.write("[+] payload done\n")
fi.close()