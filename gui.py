from tkinter import *
from PIL import ImageTk,Image


# main window settings
root = Tk()
root.title("SafeLocker")
root.geometry("500x500")

def Panda():
        
    #add an "if" statement once transceiver code is in to check whether id was found in the database 
    def PmessageWin():
        top = Toplevel()
        top.geometry("300x300")
        test = Label(top, text = "You're in!")
        
        #placing it onto the screen
        test.grid(row=1, column= 0)
        
        close = Button(top, text = "exit",command = top.destroy)
        
        #placing it onto the screen
        close.grid(row=2, column = 0)
    
    idnumber = Entry(root, width = 20, borderwidth = 3)
    myLabel2 = Label(root, text = "Please swipe your mycoyote card")

    
    
    myLabel2.grid(row=1, column= 1)
    idnumber.grid(row=2, column= 1)
    insert_button = Button(root, text = "enter", command = PmessageWin)
    insert_button.grid(row=2, column=2)

    
def Jazz():
    def JmessageWin():
        Jtop = Toplevel()
        Jtop.geometry("300x300")
        test = Label(Jtop, text = "You're in!")
        
        #placing it onto the screen 
        test.grid(row=1, column= 0)
        
        close = Button(Jtop, text = "exit", command = Jtop.destroy)
        
        #placing it onto the screen 
        close.grid(row=2, column = 0)
        

    idnumber2 = Entry(root, width = 20, borderwidth = 3)
    myLabel3 = Label(root, text = "Please swipe your mycoyote card")
    
    myLabel3.grid(row=3, column= 1)
    idnumber2.grid(row=4, column= 1)
    insert_button2 = Button(root, text = "enter", command = JmessageWin)
    insert_button2.grid(row=4, column=2)

#declaring widgets
myLabel= Label(root, text = "Welcome Back! Please select a locker")
myButton = Button(root, text= "Panda", padx = 50, pady = 50, fg = "Blue", command = Panda)
myButton2 = Button(root, text= "Jazzz", padx = 50, pady = 50, fg = "Blue",command = Jazz)


#placing in onto the screen
myLabel.grid(row=0, column=1)
myButton.grid(row=1, column=0) 
myButton2.grid(row=3, column=0)

#Loops unil we close window
root.mainloop()
