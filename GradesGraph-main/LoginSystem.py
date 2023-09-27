#importing neccesary modules to create a GUI
from tkinter import *
import tkinter as tk
from tkinter import messagebox

#import for the database
import psycopg2 

#import userclass for interface
from user import *

def loginsystem():
    loginsystem = Tk()
    loginsystem.title("Login or Register")
    loginsystem.resizable(0,0)
    
    global name, nameEntry
    global pword, pwordEntry

    #global variable for username and password entry to work throughout all functions without redefining each time.
    name = StringVar(loginsystem)
    pword = StringVar(loginsystem)

    def createUser():
        db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s;", (name.get(),)) 
        
        if cursor.fetchone() is not None:
            #user is existing in the database
            messagebox.showerror("System", "This user is already registered.")
        else: 
            cursor.execute("INSERT INTO users (user_id, username, password) VALUES (DEFAULT, %s, %s);", (name.get(), pword.get()))
            db.commit()
            messagebox.showinfo("System", "You have been registered.")
            
        db.commit()
        db.close()

        #This funciton is designed to be used when creating a new user and uses databases to store the username and password entries.

    def checkUser():
        db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s;", (name.get(),)) 
        
        if cursor.fetchone() is None:
            #user is existing in the database
            messagebox.showerror("System", "This user is not registered.")
        else: 
            cursor.execute("SELECT password FROM users WHERE username = %s;", (name.get(),)) 
            if pword.get() in cursor.fetchone():
                #users credentials are correct so they can log in
                messagebox.showinfo("System", "Logged in.")
                userclass = user(name.get(), pword.get())
                userclass.send(loginsystem)
            else:
                messagebox.showinfo("System", "Incorrect password.")
        db.commit()
        db.close()

    #creating the signup button and using the grid command to put the button at desired area in tkinter.
    Label(loginsystem, text='Username: ').grid(row=1,column=0,sticky=W,padx=5, pady=5)
    Label(loginsystem, text='Password: ').grid(row=2,column=0,sticky=W,padx=5, pady=5)
    
    #Defining the visible prompts for the user contuining to use the grid function to place the labels in the desired position.
    nameEntry = Entry(loginsystem,textvariable = name)
    pwordEntry = Entry(loginsystem,textvariable = pword,show='*')
    nameEntry.grid(row=1,column=1)
    pwordEntry.grid(row=2,column=1)
    
    #this allows the user to enter a username and password for it to be checked later on.
    signupButton = Button(loginsystem,text="Signup",bg='#153060',command=createUser)
    signupButton.grid(row=3,column=0, padx=5, pady=5)

    loginButton = Button(loginsystem, text='Login',bg='#153060',command=checkUser)
    loginButton.grid(row=3,column=3,sticky=E,padx=5, pady=5)
    loginsystem.mainloop()
    #The signup button to allow the user to progress and create the user using the button feature

def main():
    db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
    cursor = db.cursor()

    #this creates the students table if it doesnt exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50),
                    password VARCHAR(1000)
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS grades (
                    grade_id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    grade VARCHAR(2),
                    mock_name VARCHAR(150)
                    );""")
    db.commit()
    db.close()
    loginsystem()

main()