#!/usr/bin/python3
import socket
import sys
from _thread import *
import cv2 as cv
import winsound
import webbrowser

# https://stackoverflow.com/questions/25782600/sending-video-stream-from-server-to-client-using-socket-programming-in-python

host = ''  # Tahendab sumboolselt koiki
port = int(input("Sisesta pordi number: "))
numconn = 2  # Samaaegsete uhenduste hulk
buffer_size = 4096
vastus = "Sain info kätte"
frequency = 37
duration = 1000


def heli():
    webbrowser.open("http://192.168.50.182:8888/html/")
    winsound.MessageBeep()


def clientthread(conn):
    conn.send("Serveriga ühendatud".encode())
    while True:
        try:
            andmed = conn.recv(buffer_size)
            print(andmed)
            if andmed.decode() == "2":
                break
            if andmed.decode() == "1":
                heli()
                while True:
                    käsk = input("Kas lasta sisse (1) või ei(0)?").strip()
                    if käsk == "1":
                        conn.send(käsk.encode())
                        break
                    if käsk == "0":
                        conn.send(käsk.encode())
                        break
        except socket.error as msg:
            print("Threadiviga Veakood: " + str(msg.args[0]) + "Veakirjeldus: " + msg.args[1])
            break
    print("läksin välja")
    conn.close()


pesa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pesa.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Pesa on loodud")

try:
    pesa.bind((host, port))
except socket.error as msg:
    print("Sidumise Veakood:" + str(msg.args[0]) + "Veakirjeldus: " + msg.args[1])
    pesa.close()
    sys.exit()

print("Pesa on seotud")
pesa.listen(numconn)
print("Pesa kuulab nuud")

try:
    while True:
        conn, addr = pesa.accept()
        print("Uhendus " + addr[0] + ":" + str(addr[1]))
        start_new_thread(clientthread, (conn,))

except KeyboardInterrupt:
    pesa.close()
    sys.exit()
