from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import psycopg2 

#creates the graph
import matplotlib.pyplot as plt

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self): #this would return the username
        return self.username
    
    def getPassword(self):  #this would return the user's password
        return self.password

    def send(self, window):
        window.destroy()
        gtp = { "A*": 6, "A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "U": 0 }

        def addGrade():
            db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
            cursor = db.cursor()
            addgrade = Toplevel(wind)

            grade = StringVar(addgrade)
            grade.set("choose a grade")

            gradeLabel = Label(addgrade, text = "Grade: ")
            gradeLabel.grid(column=0,row=0)

            grades = ["A*","A","B","C","D","E","U"]
            gradeList = OptionMenu(addgrade, grade, *grades)
            gradeList.grid(column=1,row=0)

            mock = StringVar(addgrade)

            mockLabel = Label(addgrade, text = "Mock: ")
            mockLabel.grid(column=0,row=1)

            mockEntry = Entry(addgrade,textvariable = mock)
            mockEntry.grid(column=1,row=1)

            def setgrade():
                if grade.get() != "choose a grade":
                    if mock.get().strip() == "":
                        cursor.execute("SELECT user_id FROM users WHERE username = %s;", (self.getUsername(),))
                        user = cursor.fetchone()
                        cursor.execute("INSERT INTO grades (grade_id, user_id, grade, mock_name) VALUES (DEFAULT, %s, %s, %s);", (user[0],grade.get(),"untitled mock",))
                        db.commit()
                        messagebox.showinfo("System","Grade was set")
                    else:
                        cursor.execute("SELECT user_id FROM users WHERE username = %s;", (self.getUsername(),))
                        user = cursor.fetchone()
                        cursor.execute("INSERT INTO grades (grade_id, user_id, grade, mock_name) VALUES (DEFAULT, %s, %s, %s);", (user[0],grade.get(),mock.get(),))
                        db.commit()
                        messagebox.showinfo("System","Grade was set")

            Button(addgrade, text = "Add Grade", height = "2", width = "10", command = setgrade).grid()
            db.commit()
            db.close

        def checkGrade():
            db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
            cursor = db.cursor()
            
            cursor.execute("SELECT user_id FROM users WHERE username = %s;", (self.getUsername(),))
            userid = cursor.fetchone()

            cursor.execute("SELECT mock_name, grade FROM grades WHERE user_id = %s;", (userid[0],))
            mockandgrades = cursor.fetchall()

            db.close()
            
            x = []
            y = []
            count = 0
            for mockname in mockandgrades:
                mock = mockname[0]
                if mock != "untitled mock":
                    x.append(mock)
                else:
                    count = count + 1
                    x.append("mock(U) " + str(count))

                y.append(gtp[mockname[1]])

            plt.bar(x, y, color='red', width = 0.6)
            plt.plot(x, y, color='black', marker='d')

            axes = plt.gca()
            axes.set_ylim([0,6])
            axes.set_yticks([0,1,2,3,4,5,6])

            axes.set_yticklabels(["U","E","D","C","B","A","A*"])
            plt.xlabel('mock')
            plt.ylabel('grade') 
            plt.title('grades')
            plt.show()


        def getPredictedGrade():
            def predict(gpa):
                if gpa+1 >= 6:
                    return "A*"
                else:
                    for grade in ["A", "B", "C", "D", "E", "U"]:
                        if gpa+1 == gtp[grade]:
                            return grade
                            
            counter = 0
            usergrades = []

            db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
            cursor = db.cursor()
            
            cursor.execute("SELECT user_id FROM users WHERE username = %s;", (self.getUsername(),))
            userid = cursor.fetchone()

            cursor.execute("SELECT grade, mock_name FROM grades WHERE user_id = %s;", (userid[0],))
            grades = cursor.fetchall()

            for grade in grades:
                usergrades.append([grade[0], grade[1]])
                counter = counter + gtp[grade[0]]
            
            if len(usergrades) == 0:
                gpa = 0
            else:
                gpa = math.floor(counter/len(usergrades))
            
            pwind = Toplevel(wind)
            gradeT = ttk.Treeview(pwind)
            gradeT["columns"] = ("grades")
            gradeT.column("grades", width=200)
            gradeT.heading("grades", text="grades")

            for i in range(len(usergrades)):
               gradeT.insert("", "end", text= usergrades[i][1] + " Grade", values = (usergrades[i][0]))

            predicted = predict(gpa)
            gradeT.insert("", "end", text="Predicted Grade", values = (predicted))

            gradeT.grid()
            db.close

        wind = Tk()
        wind.title("Main System")
        addGradeButton = Button(text = "Add Grade", height = "6", width = "30", command = addGrade)
        checkGradeButton = Button(text = "Check Grades", height = "6", width = "30", command = checkGrade)
        predictGradeButton = Button(text = "Predicted Grade", height = "6", width = "30", command = getPredictedGrade)
        addGradeButton.grid(padx=5, pady=5) 
        checkGradeButton.grid(padx=5, pady=5) 
        predictGradeButton.grid(padx=5, pady=5) 

        def passw():
            change = password(self.getUsername(), self.getPassword())
            change.changePassword()

        menu = Menu(wind)
        settingsMenu = Menu(menu, tearoff = 0)
        settingsMenu.add_command(label = "Change Password", command = passw)
        menu.add_cascade(label = "Settings", menu = settingsMenu)

        wind.config(menu = menu)
        wind.mainloop()

class password(user):
    def changePassword(self):
        wind = Tk()
        wind.title("Change password")
        global old, new
        old = StringVar(wind)
        new = StringVar(wind)

        Label(wind, text="Old password: ").grid(row=1,column=0,sticky=W,padx=5, pady=5)
        Label(wind, text="New password: ").grid(row=2,column=0,sticky=W,padx=5, pady=5)
        
        oldpasswordEntry = Entry(wind,textvariable = old)
        newpasswordEntry = Entry(wind,textvariable = new,show='*')
        oldpasswordEntry.grid(row=1,column=1, padx=5, pady=5)
        newpasswordEntry.grid(row=2,column=1)
        
        def setPassword():
            db = psycopg2.connect(host = "localhost", user = "postgres", password = "postgres", port = "5432", database = "grades")
            cursor = db.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s;", (self.getUsername(),))
            storedpassword = cursor.fetchone()

            if old.get() in storedpassword:
                if new.get() == storedpassword[0]:
                    messagebox.showerror("System", "The new password cannot be the same as your old one.")
                else:
                    cursor.execute("UPDATE users SET password = %s WHERE username = %s;", (new.get(), self.getUsername(),))
                    messagebox.showinfo("System", "The password was changed to " + new.get())
                    db.commit()
                    wind.destroy()
            else:
                messagebox.showinfo("System", "The old password is incorrect.")

            db.close()
        changeButton = Button(wind,text="Change password",bg="#153060", command=setPassword)
        changeButton.grid(row=3,column=0, padx=5, pady=5)

        wind.mainloop()