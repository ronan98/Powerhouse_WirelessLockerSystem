# -*- coding: utf-8 -*-
"""
PowerHouse
Wireless Locker Project
Ronan | Heidy | Justin | Faisal | Abdullah
"""

import time
import sys
import paho.mqtt.publish as publish
import sqlite3
from tkinter import *
from PIL import ImageTk, Image


def unlockDoor():
    locker = (input("Which locker would you like to open?"))
    print(locker)

    if(locker == '1'):
        if(locker1_access == True):
            publish.single("unlockNUM", locker, hostname="192.168.1.41")
        else:
            print("Access denied")
    elif(locker == '2'):
        if(locker2_access == True):
            publish.single("unlockNUM", locker, hostname="192.168.1.41")
        else:
            print("Access denied")
    else:
        print("Locker does not exist")

def login():

    global ID
    global locker1_access
    global locker2_access

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    ID = input("Enter ID")

    c.execute("SELECT * FROM users WHERE user_ID = (?)", (ID,))
    items = c.fetchone()
    if items is None:
        print("There is no ID %s"%ID)
        return
    else:
        locker1_access = bool(items[2])
        locker2_access = bool(items[3])

    conn.commit()
    conn.close()

    unlockDoor()
        
def newUser():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    user_info = [
                    input("Swipe your coyote ID."), 
                    input("Password"),
                    input("Access to Locker1?"),
                    input("Access to Locker2?")
                ]
    
    c.execute("INSERT OR REPLACE INTO users VALUES(?,?,?,?)", user_info)
    conn.commit()
    conn.close()
    
# def openLocker():
#     locker, bool = authentication()
#     unlockDoor(locker, bool)


def main():

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    items = c.fetchall()
    for item in items:
        print(item[0] + " " + item[1]+ " " + str(item[2]) + " " + str(item[3]))
    
    print("-------------------------------------------")
    print("To close the program, press CTRL+C")
    print("-------------------------------------------\n")
    
    selection = 0

    while True:
        print("Enter your selection. 1 to open locker, 2 to create a new user, 3 to exit the program.")
        selection = input()
        
        if selection == '1':
            login()
        elif selection == '2':
            newUser()
        elif selection == '3':
            sys.exit()
        else:
            print("Selection invalid.")
            
if __name__ == '__main__':
    main()
        
        
