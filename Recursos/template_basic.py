#!/usr/bin/env python3

from struct import pack, unpack
import sys, subprocess, socket

def p32(val): return pack("<I",val)
def p64(val): return pack("<Q",val)
def u32(val): return unpack("<I",val)
def u64(val): return unpack("<Q",val)

bin = "binary"
domain = "domain.com"
port = 4444

def start():
    if len(sys.argv) > 1 and sys.argv[1] == "REMOTE":
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((domain,port))
        return s
    else:
        return subprocess.Popen([bin],
         stdin=subprocess.PIPE,
         stdout=subprocess.PIPE,
         stderr=subprocess.PIPE,)

r = start()

# --- Your code goes here ---




