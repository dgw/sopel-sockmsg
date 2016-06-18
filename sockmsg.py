"""
sockmsg.py - Sopel module example for sending text received over TCP socket to IRC
Copyright (c) 2016 dgw, https://dgw.me/
Licensed under the GNU Public License (GPL) v3.0
"""

from sopel import module
from sopel import tools
import socket
import threading

HOST   = '127.0.0.1'
PORT   = 7675  # SOPL
TARGET = '#dgw'

sock = None


def setup(bot):
    global sock
    if sock:  # the socket will already exist if the module is being reloaded
        return
    sock = socket.socket()  # the default socket types should be fine for sending text to localhost
    try:
        sock.bind((HOST, PORT))
    except socket.error as msg:
        print "socket fucked up: " + str(msg[0]) + ": " + msg[1]
        return
    sock.listen(5)


def shutdown(bot):
    global sock
    sock.close()
    sock = None  # best to be explicit about things


def receiver(conn, bot):
    buffer = ''
    while True:
        data = conn.recv(2048)
        buffer += data
        if not data:
            conn.close()
            break
        if '\n' in buffer:
            data, _, buffer = buffer.rpartition('\n')
            sayit(bot, data)
    sayit(bot, buffer)


def sayit(bot, data):
    for line in data.splitlines():
        bot.say("[sockmsg] %s" % line, TARGET)


# Start listener on welcome RPL, which should only ever be received once
@module.event(tools.events.RPL_WELCOME)
@module.rule('.*')
def listener(bot, trigger):
    global sock
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=receiver, args=(conn, bot), name='sockmsg-listener').start()
