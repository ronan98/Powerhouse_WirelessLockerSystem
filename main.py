from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import messagebox
import paho.mqtt.publish as publish
import sqlite3

conn = sqlite3.connect('user.db')

# Create a cursor
c = conn.cursor()

# Create a table
c.execute("""CREATE TABLE IF NOT EXISTS users(
		user_ID text primary key,
		password text,
		locker1 integer NOT NULL DEFAULT 0 CHECK(locker1 IN (0,1)),	
		locker2 integer	NOT NULL DEFAULT 0 CHECK(locker2 IN (0,1))	
	)""")

# Commit our command
conn.commit()

# Close the connection
conn.close()

class PowerhouseApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("720x480")
        self.iconbitmap('icon.ico')
        self.title("Remote Locker GUI")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg='')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, LoginPage, LockerSelect, createUser):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.photo = PhotoImage("bg.pgm")
        mainTitle = Canvas(self, width=720, height=75)
        mainTitle.create_text(360,0, font=('arial',40,'bold'), fill='grey', text="Remote Locker Access", anchor="n")
        mainTitle.grid(column=0, row=0, columnspan=3)

        button1 = Button(self, text="Login", font=('arial',15,'bold'), fg='blue', height=1, width=10, command=lambda: controller.show_frame("LoginPage"))
        button1.grid(column=0,row=2, pady=50)
        button2 = Button(self, text="New User", font=('arial',15,'bold'), fg='blue', height=1, width=10, command=lambda: controller.show_frame("createUser"))
        button2.grid(column=1,row=2, pady=50)
        button3 = Button(self, text="Exit", font=('arial',15,'bold'), fg='blue', height=1, width=10, command=parent.quit)
        button3.grid(column=2,row=2, pady=50)



    def quit(parent):
        parent.destroy()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        mainTitle = Canvas(self, width=720, height=75)
        mainTitle.create_text(360,0, font=('arial',40,'bold'), fill='grey', text="User Login", anchor=N)
        mainTitle.grid(column=0, row=0, columnspan=3)
        label1 = Label(self, font=('arial',15,'bold'), fg='blue',text="Swipe Coyote ID:")
        label1.grid(column=0, row=1, pady=60, padx=30)
        self.IDEntry = Entry(self, width=30)
        self.IDEntry.grid(column=0, row=1, columnspan=3, rowspan=1, pady=50)
        button1 = Button(self, text="Enter", font=('arial',10,'bold'), fg='blue', command= lambda:[self.getID(), self.clearEntry()])
        button1.grid(column=2, row=1, pady=50, padx=(0,80),sticky="w")
        button2 = Button(self, text="Home", font=('arial',15,'bold'), fg='blue', height=1, width=8, command=lambda:[controller.show_frame("HomePage"), self.clearEntry()])
        button2.grid(column=2, row=0, sticky='e', padx=(0,20))

    def clearEntry(self):
    	self.IDEntry.delete(0, END)

    def getID(self):
    	global locker1_access
    	global locker2_access

    	locker1_access = False
    	locker2_access = False

    	conn = sqlite3.connect('user.db')
    	c = conn.cursor()

    	ID = self.IDEntry.get()

    	c.execute("SELECT * FROM users WHERE user_ID = (?)", (ID,))
    	items = c.fetchone()
    	if items is None:
            print("There is no ID %s"%ID)
            messagebox.showwarning("Error", "ID was not found in records.")
            return
    	else:
            locker1_access = bool(items[2])
            locker2_access = bool(items[3])
            print("success")
            self.controller.show_frame("LockerSelect")

    	conn.commit()
    	conn.close()



class LockerSelect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        mainTitle = Canvas(self, width=720, height=75)
        mainTitle.create_text(360,0, font=('arial',50,'bold'), fill='blue', text="Select Locker", anchor=N)
        mainTitle.config(bg='white')
        mainTitle.grid(column=0, row=0, columnspan=2)
        button1 = Button(self, text="Home", font=('arial',15,'bold'), fg='blue', height=1, width=8, command=lambda: controller.show_frame("HomePage"))
        button1.grid(column=1, row=0, sticky='e', padx=(0,20))

        locker1_btn = Button(self, text="Locker1", font=('arial',15,'bold'), fg='blue', height=1, width=8, command= lambda: self.unlock('1'))
        locker2_btn = Button(self, text="Locker2", font=('arial',15,'bold'), fg='blue', height=1, width=8, command= lambda: self.unlock('2'))
        locker1_btn.grid(column=0, row=2, pady=50)
        locker2_btn.grid(column=1, row=2, pady=50)


    def unlock(self, locker):
        if(locker == '1'):
            if(locker1_access == True):
                print("unlocking")
                publish.single("unlockNUM", locker, hostname="47.150.252.149")
                messagebox.showinfo(title=None,message="Locker 1 unlocked!")
            else:
                print("Access denied")
                messagebox.showwarning("Error", "You do not have access to this locker!")
        elif(locker == '2'):
            if(locker2_access == True):
                print("unlocking")
                publish.single("unlockNUM", locker, hostname="47.150.252.149")
                messagebox.showinfo(title=None,message="Locker 2 unlocked!")
            else:
                print("Access denied")
                messagebox.showwarning("Error", "You do not have access to this locker!")
        else:
            print("Locker does not exist!")

class createUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        mainTitle = Canvas(self, width=720, height=65)
        mainTitle.create_text(360,0, font=('arial',35,'bold'), fill='grey', text="Create/Update User", anchor=N)
        mainTitle.grid(column=0, row=0, columnspan=2)

        button1 = Button(self, text="Home", font=('arial',15,'bold'), fg='blue', height=1, width=8, command=lambda:[controller.show_frame("HomePage"), self.clearEntry()])
        button1.grid(column=1, row=0, sticky='e', padx=(0,20))


        #entry bars and checkboxes
        self.id_entry = Entry(self, width=50)
        self.id_entry.grid(row=1, column=1, pady=10)
        # pw_entry = Entry(self, width=50, textvariable=PWvar)
        # pw_entry.grid(row=2, column=1, pady=10)
        self.LOCK1var = IntVar()
        self.locker1_chk = Checkbutton(self, variable=self.LOCK1var)
        self.locker1_chk.grid(row=3, column=1, pady=10)
        self.LOCK2var = IntVar()
        self.locker2_chk = Checkbutton(self, variable=self.LOCK2var)
        self.locker2_chk.grid(row=4, column=1, pady=10)

        #labels
        id_label = Label(self, text="Coyote ID")
        id_label.grid(row=1, column=0, pady=10)
        # pw_label = Label(self, text="Password")
        # pw_label.grid(row=2, column=0, pady=10)
        lock1_label = Label(self, text="Locker 1")
        lock1_label.grid(row=3, column=0, pady=10)
        lock2_label = Label(self, text="Locker 2")
        lock2_label.grid(row=4, column=0, pady=10)

        #submit
        submit_btn = Button(self, text="Submit", font=('arial',15,'bold'), fg='blue', height=1, width=8, command= lambda:[self.submit(), self.clearEntry()])
        submit_btn.grid(row=5, column=0, columnspan=2, pady=100)

    def clearEntry(self):
    	self.id_entry.delete(0, END)
    	self.LOCK1var.set(0)
    	self.LOCK2var.set(0)

    def submit(self):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()

        c.execute("INSERT OR REPLACE INTO users VALUES (:ID, :PW, :lock1, :lock2)",
                {
                    'ID' : self.id_entry.get(),
                    'PW' : '',
                    'lock1' : self.LOCK1var.get(),
                    'lock2' : self.LOCK2var.get()
                })

        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = PowerhouseApp()
    app.mainloop()