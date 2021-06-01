#!/usr/bin/python3
import socket
import sys
from _thread import *
import RPi.GPIO as GPIO
import time
from gpiozero import Servo

GPIO.setmode(GPIO.BOARD)
nupp = 11
led = 13
motor = 33
# servo = Servo(33)
GPIO.setwarnings(False)
GPIO.setup(nupp, GPIO.IN)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motor, GPIO.OUT)
conn = 1
pwm = GPIO.PWM(motor, 50)
pwm.start(0)

# https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/
"""def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(motor, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(motor, False)
    pwm.ChangeDutyCycle(0)
"""

time.sleep(0.1)
try:
    host = input("Sisesta host: ")
    port = int(input("Sisesta pordi nuber: "))
    buffer_size = 4096
    message = "Tere, siin klient"

    try:
        pesa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg1:
        print("Ebaonnestus pesa tegemine, veakood: " + str(msg1[0]) + " ,veasonum: " + msg1.args[1])
        sys.exit()
    print("Pesa on loodud")

    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Host IPd ei saadud")
        sys.exit()
    print("Hosti " + host + " IP aadress on " + remote_ip)
    pesa.connect((remote_ip, port))

    try:
        pesa.sendall(message.encode())
        reply = pesa.recv(buffer_size).decode()
        print("Serveri vastus: " + reply)
    except socket.error as msg1:
        print("Tekkis viga kood: " + str(msg1.args[0]) + " kirjeldus: " + msg1.args[1])
        sys.exit()
    try:
        while True:
            if GPIO.input(nupp) == GPIO.HIGH:
                GPIO.output(led, GPIO.HIGH)
                pesa.sendall("1".encode())
                andmed = pesa.recv(buffer_size).decode()
                if andmed == "1":
                    print("Sai sisendi kätte, teen lahti")
                    # set_angle(90)
                    # servo.min()

                    GPIO.output(motor, True)
                    pwm.ChangeDutyCycle(10)
                    time.sleep(0.5)
                    pwm.ChangeDutyCycle(0)
                    time.sleep(5)
                    # pwm.ChangeDutyCycle(19)
                    # time.sleep(0.5)
                    pwm.ChangeDutyCycle(20)
                    time.sleep(0.5)
                    GPIO.output(motor, False)
                    pwm.ChangeDutyCycle(0)

                    # set_angle(0)
                    # servo.mid()

                    GPIO.output(led, GPIO.LOW)

                if andmed == "0":
                    # do nothing
                    print("no ei saa sisse")
                    GPIO.output(led, GPIO.LOW)
                time.sleep(5)

    except:
        print("error")
        pesa.sendall("2".encode())
        time.sleep(0.01)
        pwm.stop()
        pesa.close()
        GPIO.cleanup()
        sys.exit()


except KeyboardInterrupt:
    pesa.sendall("2".encode())
    time.sleep(0.01)
    pwm.stop()
    pesa.close()
    GPIO.cleanup()
    sys.exit()

