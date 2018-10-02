from tkinter import *
from tkinter.ttk import *
import sys
import subprocess
import pymysql
import re



class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()

    def initUI(self):
        self.parent.title("Swipe your card")
        self.pack(fill=BOTH, expand=1)

        Style().configure("TButton", padding=(0, 2, 0, 2), 
         font='serif 10')
        
        xPlace = 75
        
        userLabel=Label(self, text = "Username:")
        userLabel.place(x=xPlace-60,y=10)
        
        self.user_entry = Entry(self, width=10)
        self.user_entry.place(x=xPlace,y=10)
        

        userpwLabel=Label(self, text = "Swipe:")
        userpwLabel.place(x=xPlace-60,y=50)
        
        self.pw_entry = Entry(self, width=20)
        self.pw_entry.place(x=xPlace,y=50)
        
        userFLLabel=Label(self, text = "")
        userFLLabel.place(x=xPlace,y=200)

        self.regiButton = Button(self, text = "OK",command=lambda: regiUser.makeUser(self.user_entry.get(),self.pw_entry.get(),self))
        self.regiButton.place(x=xPlace,y=100)







def main():
  
    main = Tk()
    main.geometry("400x200+400+400")
    app = Main(main)
    main.mainloop()  


if __name__ == '__main__':
    main()
