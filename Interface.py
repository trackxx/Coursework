from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Database import Database
import re


# The main Interface class. The window frame is instantiated here and the log-in menu given on startup.
# Creating more methods and linking them in-between expands the program.
class Interface():

    def __init__(self, parent):
        self.window = Frame(parent)     # Main window frame initialized
        self.window.grid()
        self.container = Frame(self.window)     # Container window frame initialized - used to clear window
        self.container.grid()
        self.startup()
        self.database = Database("credentials.db")

    def clearWindow(self):
        self.container.grid_forget()
        self.container = Frame(self.window)
        self.container.grid()
        self.errMessage = Message(self.container, font=('MS', 10), fg='red', width="320")
        self.errMessage.config(justify="center")

    def startup(self):

        # Initialized widgets
        lblUsername = Label(self.container, text='Username:', font=('MS', 10))
        lblPassword = Label(self.container, text='Password:', font=('MS', 10))
        lblRepeat = Label(self.container, text='Repeat Password:', font=('MS', 10))
        lblCourse = Label(self.container, text='Your Course:', font=('MS', 10))
        lblOr = Label(self.container, text='or', font=('MS', 10))
        lblID = Label(self.container, text='Student ID:', font=('MS', 10))
        btnLogIn = Button(self.container, text='Log-In', font=('MS', 10))
        btnRegister = Button(self.container, text='Register', font=('MS', 10))
        btnOpenLogIn = Button(self.container, text='Open log-in Form', font=('MS', 10))
        btnOpenReg = Button(self.container, text='Open Registration Form', font=('MS', 10))
        self.errMessage = Message(self.container, font=('MS', 10), fg='red', width="320")
        self.entUsername = Entry(self.container)
        self.entPassword = Entry(self.container, show="*")
        self.entRepeat = Entry(self.container, show="*")
        self.entID = Entry(self.container)
        self.cmbCourse = ttk.Combobox(self.container, width=17, state="readonly")

        # Widget configuration
        lblUsername.grid(row=0, column=0, padx=10, pady=5, sticky=E)
        self.entUsername.grid(row=0, column=1, padx=10)
        lblPassword.grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.entPassword.grid(row=1, column=1)
        btnLogIn.grid(row=2, column=0, columnspan=2, pady=10)
        lblOr.grid(row=3, column=0, columnspan=2, pady=5)
        btnOpenReg.grid(row=4, column=0, columnspan=2, pady=10)
        self.cmbCourse['values'] = ["Computer Science"]
        self.errMessage.config(justify="center")

        def openRegistration():
            self.errMessage.grid_forget()
            btnLogIn.grid_forget()
            btnOpenReg.grid_forget()
            lblRepeat.grid(row=2, column=0, padx=10, pady=5, sticky=E)
            self.entRepeat.grid(row=2, column=1)
            lblID.grid(row=3, column=0, padx=10, pady=5, sticky=E)
            self.entID.grid(row=3, column=1)
            lblCourse.grid(row=4, column=0, padx=10, pady=5, sticky=E)
            self.cmbCourse.grid(row=4, column=1, padx=10)
            btnRegister.grid(row=5, column=0, columnspan=2, pady=10)
            lblOr.grid(row=6, column=0, columnspan=2, pady=5)
            btnOpenLogIn.grid(row=7, column=0, columnspan=2, pady=10)
            self.entUsername.delete(0, END)
            self.entPassword.delete(0, END)

        def openLogIn():
            self.errMessage.grid_forget()
            lblRepeat.grid_forget()
            self.entRepeat.grid_forget()
            btnRegister.grid_forget()
            btnOpenLogIn.grid_forget()
            lblCourse.grid_forget()
            self.cmbCourse.grid_forget()
            lblID.grid_forget()
            self.entID.grid_forget()
            btnLogIn.grid(row=2, column=0, columnspan=2, pady=10)
            lblOr.grid(row=3, column=0, columnspan=2, pady=5)
            btnOpenReg.grid(row=4, column=0, columnspan=2, pady=10)
            self.entUsername.delete(0, END)
            self.entPassword.delete(0, END)
            self.entRepeat.delete(0, END)
            self.entID.delete(0, END)
            self.entPassword.option_clear()

        def tryLogIn():
            if self.logIn():
                self.clearWindow()
                self.createMenu(self.entUsername.get())

        def tryRegister():
            if self.register():
                openLogIn()             # Go back to log-in

        # Widget actions
        btnLogIn['command'] = tryLogIn
        btnRegister['command'] = tryRegister
        btnOpenReg['command'] = openRegistration
        btnOpenLogIn['command'] = openLogIn

    # Function to check user credentials and proceed with logging in when 'log-in' button is pressed.
    # Performs checks on user input.
    def logIn(self):
        username = self.entUsername.get()
        password = self.entPassword.get()

        if len(username) == 0 or len(password) == 0:
            self.errMessage.grid(row=5, columnspan=2)
            self.errMessage.config(text="You must complete all login fields!")
            return False

        if len(password) < 8:
            self.errMessage.grid(row=5, columnspan=2)
            self.errMessage.config(text="Password is at least 8 characters!")
            return False

        if not self.database.getUser(username, password):
            self.errMessage.grid(row=5, columnspan=2)
            self.errMessage.config(text="Invalid username/password.")
            return False

        # User is now logged in
        return True

    # Function to register user when 'register' button is pressed. Performs checks on user input.
    def register(self):
        username = self.entUsername.get()
        password = self.entPassword.get()
        passwordRep = self.entRepeat.get()
        course = self.cmbCourse.get()
        id = self.entID.get()

        # Checks regarding registration fields are made here
        if len(username) == 0 or len(password) == 0 or len(passwordRep) == 0 or len(course) == 0 or len(id) == 0:
            self.errMessage.grid(row=8, columnspan=2)
            self.errMessage.config(text="You must complete all registration fields!")
            return False

        if self.database.getUsername(username):
            self.errMessage.grid(row=8, columnspan=2)
            self.errMessage.config(text="This username already exists!")
            return False

        if len(password) < 8:
            self.errMessage.grid(row=8, columnspan=2)
            self.errMessage.config(text="Password must be at least 8 characters long!")
            return False

        if password != passwordRep:
            self.errMessage.grid(row=8, columnspan=2)
            self.errMessage.config(text="Passwords do not match!")
            return False

        if len(id) > 8 or not re.findall(r'[Cc][0-9]{7}', id):
            self.errMessage.grid(row=8, columnspan=2)
            self.errMessage.config(text="Invalid Student ID.")
            return False

        # User is registered into the database here
        self.errMessage.grid_forget()
        self.database.addEntry(username, password, course, id)
        messagebox.showinfo("Registered", "You have successfully registered! You can now log in.")
        return True

    def createMenu(self, username):
        for row in self.database.getUserData(username):
            frmCourse = Frame(self.container)
            lblID = Label(self.container, text="Student ID: " + row[2], font=('MS', 10))
            lblCourse = Label(self.container, text="Course: " + row[1], font=('MS', 10))
            lblLesson = Label(frmCourse, text="Choose lesson: ", font=('MS', 10))
            lblOr = Label(frmCourse, text='or', font=('MS', 10))
            cmbCourse = ttk.Combobox(frmCourse, width=17, state="readonly")
            btnSelect = Button(frmCourse, text='Go to Lesson', font=('MS', 10))
            btnHistory = Button(frmCourse, text='View History', font=('MS', 10))

            cmbCourse['values'] = ["Lesson 1", "Lesson 2"]

            # DELETE ME
            def select():
                if len(cmbCourse.get()) == 0:
                    print("You must choose a lesson!")
                    self.errMessage.grid(row=3, columnspan=2)
                    self.errMessage.config(text="You must choose a lesson!")
                    return
                self.clearWindow()
                print("Open Lesson Menu")

            def history():
                self.clearWindow()
                print("Open History Menu")

            btnSelect['command'] = select
            btnHistory['command'] = history

            lblID.grid(row=0, column=0, columnspan=2, sticky=W, padx=5, pady=5)
            lblCourse.grid(row=1, column=0, columnspan=2, sticky=W, padx=5)
            frmCourse.grid(row=2, columnspan=2, pady=20, padx=5)
            lblLesson.grid(row=0, column=0, sticky=W, pady=5)
            cmbCourse.grid(row=0, column=1, sticky=W, pady=5)
            btnSelect.grid(row=1, columnspan=2, pady=5)
            lblOr.grid(row=3, column=0, columnspan=2, pady=10)
            btnHistory.grid(row=4, columnspan=2, pady=5)

