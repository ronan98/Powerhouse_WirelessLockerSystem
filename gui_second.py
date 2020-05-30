from tkinter import *
import tkinter.messagebox
import sqlite3
import tkinter as tk
from csv import writer
import pandas as pd
    
def authentication():
    window2 = tk.Toplevel()
    window2.geometry("500x300")
    window2.config(bg="slate gray")
    

    canvas1 = tk.Canvas(window2, width = 400, height = 300,  relief = 'raised', bg = 'gainsboro')
    canvas1.pack()

    label1 = tk.Label(window2, text= "Authentication:")
    label1.config(font = ('helvetica', 14))
    canvas1.create_window(200, 25, window = label1)

    label2 = tk.Label(window2, text='Type your ID Number:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)

    entry1 = tk.Entry(window2) 
    canvas1.create_window(200, 140, window=entry1)

    def FindUser():
        global iD
        iD = float(entry1.get())
        
        df = pd.read_csv("users2.csv")
        df["coyoteID"]= df["coyoteID"].astype(str)
        df["locker#"]= df["locker#"].astype(str)
        value = input("Swipe your coyote ID.\n")

        def UnlockDoor():
            df = pd.read_csv("users2.csv")
            df["locker#"]= df["locker#"].astype(str)
          
            lockerName = df.loc[lockerNum, 'locker#']
            publish.single("unlockNUM", lockerName, hostname="192.168.1.41")
        
        for i in range(len(df)):
           
            if iD == df.loc[i, 'coyoteID']:
                Result = ('User found')
                label_Result = tk.Label(window2, text = Result, bg='blue')
                canvas1.create_window(270, 200, window=label_Result)
                button4 = Button(window2, font = ('arial' , 10, 'bold'),
                                 text = "Open locker !" , command = UnlockDoor)
                canvas1.create_window(200, 200, window= button4)
            else:
                Result = ('Not authorized user')
                label_Result = tk.Label(window2, text = Result, bg='blue')
                canvas1.create_window(270, 200, window=label_Result)
  

    Button3 = Button(window2, font=('arial', 10, 'bold'),
                        text= "Enter", padx = 10, pady = 10,
                               fg = "black",command = FindUser)
    canvas1.create_window(200, 200, window=Button3)


def Open_locker():
    window1 = Toplevel()
    window1.geometry("900x500")
    window1.config(bg="light grey")

    def quit_secondwindow():
        window1.destroy()

    MainFrame = Frame(window1, bg="DodgerBlue4")
    MainFrame.grid()

    #  frame for the header # 

    HeadFrame = Frame(MainFrame, bd=1, padx=300, pady=10,
                          bg='light grey',relief=RIDGE)
    HeadFrame.pack(side=TOP)
    ITitle = Label(HeadFrame, font=('arial',35,'bold'), fg = 'sea green',
                            text = 'Select a locker',bg='light grey')
    ITitle.grid()
        
    #  frame for the buttons #
        
    MiddleFrame = Frame(window1, bd=1, padx=50, pady=10,
                          bg='light grey', relief=RIDGE)
    MiddleFrame.grid()
    Button1 = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "Locker 1", padx = 30, pady = 30,
                               fg = "sea green")
    Button2 = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "Locker 2", padx = 30, pady = 30,
                               fg = "sea green")
    Button3 = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "back", padx = 30, pady = 30,
                               fg = "sea green", command = quit_secondwindow )
    Button1.pack(side=TOP, fill='both') 
    Button2.pack(fill='both')
    Button3.pack(fill='both')
        

        
def new_user():
    window2 = tkinter.Toplevel()
    window2.geometry("800x500")
def quit_progam():
    root.destroy()
 
class Main:

    def __init__(self,root):
        self.root = root
        self.root.title("SafeLocker")
        self.root.geometry("900x600")
        self.root.config(bg="grey")

 
        MainFrame = Frame(self.root,bg="white")
        MainFrame.grid()

        #  frame for the header # 

        HeadFrame = Frame(MainFrame, bd=1, padx=300, pady=10,
                          bg='white',relief=RIDGE)
        HeadFrame.pack(side=TOP)
        self.ITitle = Label(HeadFrame, font=('arial',50,'bold'), fg = 'blue',
                            text = 'Welcome ',bg='white')
        self.ITitle.grid()
        
        #  frame for the buttons #
        
        MiddleFrame = Frame(self.root, bd=1, padx=50, pady=10,
                          bg='grey', relief=RIDGE)
        MiddleFrame.grid()
        self.myButton = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "Open a locker", padx = 30, pady = 30,
                               fg = "Blue", command= authentication)
        self.myButton2 = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "Create a new user", padx = 30, pady = 30,
                               fg = "Blue", command= authentication)
        self.myButton3 = Button(MiddleFrame, font=('arial', 15, 'bold'),
                        text= "Exit the program", padx = 30, pady = 30,
                               fg = "Blue", command = quit_progam)
   
        self.myButton.pack(side=TOP, fill='both') 
        self.myButton2.pack(fill='both')
        self.myButton3.pack(fill='both')


       
if __name__ =='__main__':

    root= Tk()
    main = Main(root)
    root.mainloop()



        
