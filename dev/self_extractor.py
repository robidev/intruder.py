"""Demonstrate self extraction of data from a Python script.
**YOU PROBABLY DON'T WANT TO DO THIS**
If run with any command line arguments, this script will extract the Zen of
Python from the embedded data at the end of the script and print it to standard
out.
    $ python self_extract.py
    The Zen of Python, by Time Peters
    ...
If run with one or more command line arguments, this script writes lines
suitable for self extraction to standard out.
    $ python self_extract.py zen.txt
    #^@VGhlIFplbiBvZiBQeXRob24sIGJ5IFRpbSBQZXRlcnMKCkJlYXV0aWZ1bCBpcyBi
    ...
This script was created by appended the about output to it's self.
    $ python self_extract.py zen.txt >> self_extract.py
Possible uses include self insstalling packages.
"""
from __future__ import print_function

from base64 import b64encode, b64decode
import sys
import os

if sys.version_info[0] >= 3:
    bytes_out = sys.stdout.buffer
else:
    bytes_out = sys.stdout

# Identifies a self extaction line. b'#\x00' is better, but doesn't paste well
# into a github gist or pastebin.
# TAG = b'#\x00'
TAG = b'#~'

def bytes_slicer(length, source):
    "Iterate over slices of given length from source"
    start = 0
    stop = length
    while start < len(source):
        yield source[start:stop]
        start = stop
        stop += length

def write_extractor_lines(filename, dest=bytes_out):
    "Write a sequence of lines to dest suitable for self extraction"
    with open(filename, 'rb') as source:
        raw = source.read()
        encoded = b64encode(raw)
        for section in bytes_slicer(64, encoded):
            bytes_out.write(TAG)
            bytes_out.write(section)
            bytes_out.write(b'\n')

def read_extractor_lines(dest=bytes_out):
    "Read self extraction lines from this script and write to dest"
    script = os.path.abspath(sys.argv[0])
    with open(script, 'rb') as source:
        for line in source:
            if not line.startswith(TAG):
                continue
            bytes_out.write(b64decode(line[len(TAG):-1]))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            write_extractor_lines(filename)
    else:
        read_extractor_lines()

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