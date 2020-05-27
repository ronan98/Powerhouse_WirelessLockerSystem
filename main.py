# -*- coding: utf-8 -*-
"""
PowerHouse
Wireless Locker Project
Ronan | Heidy | Justin | Faisal | Abdullah
"""

import time
import pandas as pd
import serial
from csv import writer
import sys
import paho.mqtt.publish as publish

exit_Program = False

# to be called if a locker needs to be opened
def unlockDoor(lockerNum, status):
    if status == True:
        #print("unlocking")
        df = pd.read_csv("users2.csv")
        df["locker#"]= df["locker#"].astype(str)
        #print(str(lockerNum) + " is the locker row")
        lockerName = df.loc[lockerNum, 'locker#']
        publish.single("unlockNUM", lockerName, hostname="192.168.1.41")
        #print(lockerName)
        print("\nYour locker has been opened!\n")
    else:
        print("\nAccess denied. ID or selected locker incorrect!\n")

def authentication():
    df = pd.read_csv("users2.csv")

    df["coyoteID"]= df["coyoteID"].astype(str)
    df["locker#"]= df["locker#"].astype(str)

    value = input("Swipe your coyote ID.\n")
    locker = input("What locker?\n")
    #print(value)
    
    for i in range(len(df)):
        print(i)
        print(str(df.loc[i, 'coyoteID']))
        if value == df.loc[i, 'coyoteID']:
            #print('authorized user')
            #print(locker)
            #print(df.loc[i, 'locker#'])
            if locker == df.loc[i, 'locker#']:
                #print('authorized locker')
                lockerNum = i
                status = True
                break
            else:
                #print('not authorized locker')
                lockerNum = 0
        else:
            lockerNum = 0
            status = False
            #print("not authorized user")
    return lockerNum, status

def appendUser(file_name, list_of_elem):
    with open(file_name, 'a+',newline='') as write_obj:
        csv_writer=writer(write_obj)
        csv_writer.writerow(list_of_elem)
        
def newUser():
    user_info = [input("Swipe your coyote ID."), input("Which locker would you like to be assigned to?")]
    
    appendUser('users2.csv', user_info)
    
def openLocker():
    locker, bool = authentication()
    unlockDoor(locker, bool)


def main():
    
    print("-------------------------------------------")
    print("To close the program, press CTRL+C")
    print("-------------------------------------------\n")
    
    selection = 0

    while True:
        print("Enter your selection. 1 to open locker, 2 to create a new user, 3 to exit the program.")
        selection = input()
        
        if selection == '1':
            openLocker()
        elif selection == '2':
            newUser()
        elif selection == '3':
            sys.exit()
        else:
            print("Selection invalid.")
            
if __name__ == '__main__':
    main()
        
        
