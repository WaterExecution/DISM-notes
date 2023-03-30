#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading
import requests as req
import sqlite3
import queue
from time import sleep, time, strftime
from mfrc522 import SimpleMFRC522
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN) # PIR Sensor
GPIO.setup(15, GPIO.IN) # Slide Switch
GPIO.setup(37,GPIO.OUT) # Servo motor
GPIO.setup(18, GPIO.OUT) # Red LED
GPIO.setup(12, GPIO.OUT) # Buzzer
servo = GPIO.PWM(37,500)
reader = SimpleMFRC522()
servo.start(0)
q = queue.Queue()
doorOpened = False

def database_conn(sql_statement):
    #  try:
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    out = cursor.fetchall()  #returns a list
    cursor.close()
    conn.commit()
    conn.close()
    return out
    #  except:
    #    print("Error")

def getRFID():
    try:
        id, text = reader.read()
        return str(id)
    except:
        print("Error")
        return
    return

def getstudentrfid():
    studentRFID = database_conn("select rfid from students;")
    return studentRFID
    
    
def gate():
    servo.start(0)
    while 1:
        valid_rfids = getstudentrfid()
        rfid_tag = getRFID()
        for rfid in valid_rfids:
            if rfid_tag == rfid[0]:
                openGate()
                while 1:
                     if motionsensor() == 1:
                         closeGate()
                         break
    servo.stop()
    GPIO.cleanup()
    sleep(0.5)
    return
    
def openGate():
    try:
        for i in range(45,101,3):
            servo.ChangeDutyCycle(i)
            sleep(0.1)
        sleep(3)
    except KeyboardInterrupt:
        return
    return
    
def closeGate():
    try:
        for i in range(100,45,-3):
            servo.ChangeDutyCycle(i)
            sleep(0.1)
        sleep(5)
    except KeyboardInterrupt:
        return
    return

def openDoor():
    global doorOpened
    q.put(0)
    if q.qsize()==1 and doorOpened == False:
        doorOpened = True
        try:
            for i in range(45,101,3):
                servo.ChangeDutyCycle(i)
                sleep(0.1)
        except KeyboardInterrupt:
            return
    sleep(4)
    q.get(0)
    return

def closeDoor():
    global doorOpened
    doorOpened = False
    try:
        for i in range(100,45,-3):
            servo.ChangeDutyCycle(i)
            sleep(0.1)
        sleep(5)
    except KeyboardInterrupt:
        return
    return

def door():
    while 1:
        valid_rfids = getstudentrfid()
        rfid_tag = getRFID()
        for rfid in valid_rfids:
            if rfid_tag == rfid[0]:
                try:
                    attendance(rfid[0],"T1111","2022-12-15 08:00")
                    #attendance(rfid[0],"T1111",strftime("%Y-%m-%d %H:%M"))# T1111 2022-12-15 08:00
                    soundThread = threading.Thread(target=sound)
                    LEDThread = threading.Thread(target=LED)
                    motorThread = threading.Thread(target=motor)
                    soundThread.start()
                    LEDThread.start()
                    motorThread.start()
                    sleep(3)
                except KeyboardInterrupt:
                    break
    return

def sound():
    GPIO.output(12,1)
    sleep(0.15)
    GPIO.output(12,0)
    return

def LED():
    GPIO.output(18,1)
    sleep(1)
    GPIO.output(18,0)
    sleep(1)
    return

def motor():
    openDoor()
    while 1:
        if q.empty() and doorOpened == True:
            closeDoor()
            break
        elif q.empty() and doorOpened == False:
            break
    return
    
def motionsensor():
    return GPIO.input(11)

def attendance(rfid, classroom, currentTime):
    database_conn(f'UPDATE attendance SET present = "P" where studentid=(SELECT studentid FROM students JOIN lesson where students.rfid="{rfid}" and classroom="{classroom}" and "{currentTime}" between date and datetime(date, ("+" || timespan))) and lessonid=(SELECT lessonid FROM students JOIN lesson where students.rfid="{rfid}" and classroom="{classroom}" and "{currentTime}" between date and datetime(date, ("+" || timespan)));')
    return

while 1:
    if GPIO.input(15):
        gate()
        exit()
    else:
        door()
        exit()


