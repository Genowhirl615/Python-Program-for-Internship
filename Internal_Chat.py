#import tkinter
#top = tkinter.Tk()
# Code to add widgets will go here...
#top.mainloop()

from tkinter import *
from tkinter.ttk import *
import sys
import subprocess
import pymysql
import re



conn = pymysql.connect(host='*',user = '*',passwd='*',db='*',port =3306)
cur = conn.cursor()
conn.commit()
reuseable = ""

class regiUser(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)     
        self.parent = parent        
        self.initUI()

    def initUI(self):
        self.parent.title("Register")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TButton", padding=(0, 2, 0, 2), 
         font='serif 10')
        
        self.xPlace = 75
        self.userLabel=Label(self, text = "Username:")
        self.userLabel.place(x=self.xPlace-60,y=10)        
        self.user_entry = Entry(self, width=10)
        self.user_entry.place(x=self.xPlace,y=10)       
        self.userpwLabel=Label(self, text = "Password:")
        self.userpwLabel.place(x=xPlace-60,y=50)       
        self.pw_entry = Entry(self, width=10)
        self.pw_entry.place(x=self.xPlace,y=50)      
        self.userFLLabel=Label(self, text = "")
        self.userFLLabel.place(x=self.xPlace,y=200)
        self.regiButton = Button(self, text = "Make",command=lambda: regiUser.makeUser(self.user_entry.get(),self.pw_entry.get(),self))
        self.regiButton.place(x=self.xPlace,y=100)

    def makeUser(x,y,self):
        test = cur.execute("select User from User where User = '%s'" % (x))
        if test == 1:
             self.userUsedLabel=Label(self,text = "User exists")
             self.userUsedLabel.place(x=75,y=200)
        elif y != "":
            sql = ("insert into User(User,Password,Saved)values('%s','%s','')" % (x,y))
            cur.execute(sql)
            conn.commit()





class chatBox(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()

    def updateChat(self,OCU):
        global CurrentUser
        OtherChatUser = OCU
        self.lbox.delete(0,END)
        cur.execute("select Message from chats Where User1 = '%s' and User2 = '%s'" % (CurrentUser,OtherChatUser))
        messageUpdates = cur.fetchall()
        for msg in messageUpdates:
           self.lbox.insert(END, msg)
        
    def sendMessage(self,OCU,event):
        global CurrentUser
        OtherChatUser = OCU
        event = CurrentUser+": "+event 
        cur.execute("insert into chats(User1,User2,Message,Saved)values('%s','%s','%s','')" % (CurrentUser,OtherChatUser,event))
        conn.commit()
        chatBox.updateChat(self,OtherChatUser)
        
    def makeListbox(self,OCU):
        global CurrentUser
        OtherChatUser = OCU
        self.lbox=Listbox(self,height = 15,width = 25)
        self.lbox.pack(pady=5)
        cur.execute("select Message from chats Where User1 = '%s' and User2 = '%s'" % (CurrentUser,OtherChatUser))
        self.messages = cur.fetchall()
        for msg in self.messages:
           self.lbox.insert(END, msg) 

        
    def initUI(self):
        global CurrentUser
        global OtherUser
        OtherChatUser = OtherUser[0]
        chatBox.makeListbox(self, OtherChatUser) 
        self.text_entry = Entry(self, width=20)
        self.text_entry.place(x=87,y=300)
        self.parent.title("%s connected with %s" %(CurrentUser, OtherChatUser))
        self.pack(fill=BOTH, expand=1)
        self.sendButton = Button(self, text = "send", command =lambda: chatBox.sendMessage(self,OtherChatUser,self.text_entry.get()))
        self.sendButton.place(x=75,y=340)

    


class UserInterface(Frame):

    
    def __init__(self, parent):
        Frame.__init__(self, parent)    
        self.parent = parent
        self.initUI()

    def nameClick(event):
        w=event.widget
        print(event)
        index = int(w.curselection()[0])
        value = w.get(index)
        global OtherUser
        OtherUser = value
        chatWindow = Tk()
        chatWindow.geometry("300x400+250+250")
        chatScreen = chatBox(chatWindow)
    
    def initUI(self):
        global CurrentUser
        usernameLabel=Label(self, text=CurrentUser)
        usernameLabel.place(x=50,y=0)
        sql = "select User from User"
        cur.execute(sql)
        genUsers = cur.fetchall()
        lb=Listbox(self,height = 10,width = 10)
        for each in genUsers:
            lb.insert(END,each)
        lb.bind('<<ListboxSelect>>',UserInterface.nameClick)
        lb.pack(pady=30)     
        self.parent.title("User List")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text = "Quit", command=sys.exit)
        quitButton.place(x=0,y=250)



class Login(Frame):

    
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()
        
    def loginVer(x,y,self):
        global CurrentUser
        CurrentUser = x
        test=cur.execute("select User from User where User = '%s' AND Password = '%s'" % (x,y))
        if test == 1:
            popUp = Tk()
            popUp.geometry("100x300")
            newWindow = UserInterface(popUp)
        elif test == 0:
            self.userFLLabel=Label(text="Not Found")
            self.userFLLabel.place(x=75,y=200)
        return   

    def spawnRegi():
        register=Tk()
        register.geometry("200x300+400+400")
        newRegister = regiUser(register)
        
    def initUI(self):
        self.parent.title("Login")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TButton", padding=(0, 2, 0, 2), 
         font='serif 10')
        xPlace = 75

        self.userLabel=Label(self, text = "Username:")
        self.userLabel.place(x=xPlace-60,y=10)
        self.user_entry = Entry(self, width=10)
        self.user_entry.place(x=xPlace,y=10)

        self.userpwLabel=Label(self, text = "Password:")
        self.userpwLabel.place(x=xPlace-60,y=50)
        self.pw_entry = Entry(self, width=10)
        self.pw_entry.place(x=xPlace,y=50)

        self.regiButton = Button(self, text = "Login",command=lambda: Login.loginVer(self.user_entry.get(),self.pw_entry.get(),self))
        self.regiButton.place(x=xPlace,y=100)
        self.regiButton = Button(self, text = "Register",command=lambda: Login.spawnRegi())
        self.regiButton.place(x=xPlace,y=150)
        self.userFLLabel=Label(self, text = "")
        self.userFLLabel.place(x=xPlace,y=200)
      


def main():
  
    login = Tk()
    login.geometry("200x200+400+400")
    app = Login(login)
    login.mainloop()  


if __name__ == '__main__':
    main()
