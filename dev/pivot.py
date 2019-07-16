#!/usr/bin/env python3

import os
import paramiko

ssh_key_filename = os.getenv('HOME') + '/.ssh/id_rsa'

jumpbox_public_addr = '168.128.52.199'
jumpbox_private_addr = '10.0.5.10'
target_addr = '10.0.5.20'

jumpbox=paramiko.SSHClient()
jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
jumpbox.connect(jumpbox_public_addr, username='root', key_filename=ssh_key_filename)

jumpbox_transport = jumpbox.get_transport()
src_addr = (jumpbox_private_addr, 22)
dest_addr = (target_addr, 22)
jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)

target=paramiko.SSHClient()
target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target.connect(target_addr, username='root', key_filename=ssh_key_filename, sock=jumpbox_channel)

stdin, stdout, stderr = target.exec_command("ifconfig")
for line in stdout.read().split(b'\n'):
  print(str(line))

target.close()
jumpbox.close()