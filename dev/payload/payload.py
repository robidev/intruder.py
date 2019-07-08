
#spawning a daemon???
#script=r.text
#exec(script)
#import subprocess
#pycode = """
#import sys
#... if sys.argv[1] == 'foo':
#...     print('bar')
#... else:
#...     print('unrecognized arg')
#... """
#>>> result = subprocess.Popen(['python', '-c', pycode, 'bar'], stdout=subprocess.PIPE)#none
#>>> print(result.stdout.decode())
#import os
#os.spawnl(os.P_DETACH, 'some_long_running_command')
#DETACHED_PROCESS = 0x00000008
#
#pid = subprocess.Popen([sys.executable, "longtask.py"],
#                       creationflags=DETACHED_PROCESS).pid