"""
sockmsg.py - Sopel module example for sending text received over TCP socket to IRC
Copyright (c) 2016 dgw, https://dgw.me/
Licensed under the GNU Public License (GPL) v3.0
"""

from sopel import module
from sopel import tools
import socket
import threading

HOST = '127.0.0.1'
PORT = 7675  # SOPL

sock = socket.socket()  # configured etc. during module startup


def setup(bot):
    global sock
    try:
        sock.bind((HOST, PORT))
    except socket.error as msg:
        print "socket fucked up: " + str(msg[0]) + ": " + msg[1]
        return
    sock.listen(5)


def shutdown(bot):
    sock.close()


def botsaydata(conn, bot):
    text = ''
    while True:
        data = conn.recv(2048)
        print 'received data from socket: %s' % data
        text += data
        if not data:
            conn.close()
            break
    bot.say("[socket message] %s" % text, '#dgw')


# Start listener on welcome RPL, which should only ever be received once
@module.event(tools.events.RPL_WELCOME)
@module.rule('.*')
def listener(bot, trigger):
    global sock
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=botsaydata, args=(conn, bot), name='socket-listener').start()
