import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import tabify, limitSize

def view_staff():
    ViewStaff = Toplevel(bg='#EDFBFF')
    w = 600 #Open top level window in centre of screen
    h = 500
    ws = ViewStaff.winfo_screenwidth()
    hs = ViewStaff.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    ViewStaff.geometry('%dx%d+%d+%d' % (w, h, x, y))
    ViewStaff.title('View Staff')
            #Display view staff widgets
    ViewStaffOptionFrame = Frame(ViewStaff, bg='#EDFBFF')
    ViewStaffOptionFrame.pack(pady=100)
    DisplayStaffButton = Button(ViewStaffOptionFrame, text='Display\nStaff', width='18', height='7',
                                command=lambda: display_staff(ViewStaff, ViewStaffOptionFrame))
    DisplayStaffButton.grid(column=0, row=0, padx=20,) #Display staff
    AddStaffButton = Button(ViewStaffOptionFrame, text='Add\nStaff', width='18', height='7',
                            command=lambda: add_staff_button(ViewStaff, ViewStaffOptionFrame))
    AddStaffButton.grid(column=1, row=0, padx=20) #Add staff
    EditStaffButton = Button(ViewStaffOptionFrame, text='Edit\nStaff', width='18', height='7',
                             command=lambda: edit_staff(ViewStaff, ViewStaffOptionFrame))
    EditStaffButton.grid(column=2, row=0, padx=20) #Edit staff
    CancelButton = Button(ViewStaffOptionFrame, text='Cancel', justify='center', width='18',
                          height='7', command=ViewStaff.destroy)
    CancelButton.grid(column=1, row=1, pady=20) #Cancel button

def display_staff(ViewStaff, ViewStaffOptionFrame):
    ViewStaff.title('View Staff - Display Staff')
    ViewStaffOptionFrame.pack_forget()
    DisplayStaffFrame = Frame(ViewStaff, bg='#EDFBFF')
    DisplayStaffFrame.pack()
    global StaffCanvas #Set up canvas to display staff records
    StaffCanvas = Canvas(DisplayStaffFrame, width='560', height='490', bg='#EDFBFF', highlightthickness=0)
    StaffCanvas.pack(side=LEFT)
    StaffGridFrame = Frame(StaffCanvas, bg='#EDFBFF')
    StaffGridFrame.pack()
    
    nextrow=0 #Display attribute headings
    Label(StaffGridFrame, text='Staff ID', bg='#EDFBFF', font='bold').grid(column=0, row=nextrow, padx='20', pady='5')
    Label(StaffGridFrame, text='Password', bg='#EDFBFF', font='bold').grid(column=1, row=nextrow, padx='20', pady='5')
    Label(StaffGridFrame, text='Forename', bg='#EDFBFF', font='bold').grid(column=2, row=nextrow, padx='20', pady='5')
    Label(StaffGridFrame, text='Surname', bg='#EDFBFF', font='bold').grid(column=3, row=nextrow, padx='20', pady='5')
    Label(StaffGridFrame, text='Position', bg='#EDFBFF', font='bold').grid(column=4, row=nextrow, padx='20', pady='5')
    nextrow=nextrow+1
    
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Fetch ALL data from database
    cursor.execute('SELECT * FROM employee')
    AllStaff = cursor.fetchall()
    for row in AllStaff: #For each record in database, display relevant attributes
        Label(StaffGridFrame, text=row[0], bg='#EDFBFF').grid(column=0, row=nextrow, padx='20')
        password = str(row[1])
        pwordlength = len(password)
        newpassword = ('0'*(4-pwordlength))+password
        Label(StaffGridFrame, text=newpassword, bg='#EDFBFF').grid(column=1, row=nextrow, padx='20')
        Label(StaffGridFrame, text=row[2], bg='#EDFBFF').grid(column=2, row=nextrow, padx='20')
        Label(StaffGridFrame, text=row[3], bg='#EDFBFF').grid(column=3, row=nextrow, padx='20')
        Label(StaffGridFrame, text=row[4], bg='#EDFBFF').grid(column=4, row=nextrow, padx='20')
        nextrow=nextrow+1 #Set next available row
    connection.commit()
    connection.close()
    
    CancelButton = Button(StaffGridFrame, text='Cancel', justify='center', width='10', height='4', command=ViewStaff.destroy)
    CancelButton.grid(row=nextrow, column=2)
    StaffScrollbar = Scrollbar(DisplayStaffFrame, orient="vertical")
    StaffScrollbar.pack(side=RIGHT, fill=Y)
    StaffCanvas.config(yscrollcommand=StaffScrollbar.set)
    StaffScrollbar.config(command=StaffCanvas.yview)
    StaffCanvas.create_window((0,0),window=StaffGridFrame)
    StaffGridFrame.bind("<Configure>",StaffCanvasScroll)

def StaffCanvasScroll(event): #Bind canvas with scrollbar
    StaffCanvas.configure(scrollregion=StaffCanvas.bbox("all"))

def add_staff_button(ViewStaff, ViewStaffOptionFrame):
    ViewStaff.title('View Staff - Add Staff')
    ViewStaffOptionFrame.pack_forget()
    AddNewStaffFrame = Frame(ViewStaff, bg='#EDFBFF')
    AddNewStaffFrame.pack(pady=50)
    Label(AddNewStaffFrame, text='ADD STAFF', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)

    Label(AddNewStaffFrame, text='Staff ID:', justify='center', font=(None, 20),
          bg='#EDFBFF').grid(row=1, column=0, padx=2, pady=2)
    NewStaffIDEntry = Entry(AddNewStaffFrame, justify='center', font=(None, 20),
                            width='15')
    NewStaffIDEntry.grid(row=1, column=1, padx=2, pady=2)
    next_staff_id(NewStaffIDEntry)
    NewStaffIDEntry['state']='disabled'

    Label(AddNewStaffFrame, text='Password:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=2, column=0, padx=2, pady=2)
    PasswordVar = StringVar()
    PasswordVar.trace('w', lambda *args: limitSize(PasswordVar, 4))
    NewPasswordEntry = Entry(AddNewStaffFrame, show='*', justify='center', font=(None, 20), width='15', textvariable=PasswordVar)
    NewPasswordEntry.grid(row=2, column=1, padx=2, pady=2)
    NewPasswordEntry.focus()

    Label(AddNewStaffFrame, text='First Name:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=3, column=0, padx=2, pady=2)
    FirstNameVar = StringVar()
    FirstNameVar.trace('w', lambda *args: limitSize(FirstNameVar, 14))
    NewFirstNameEntry = Entry(AddNewStaffFrame, justify='center', font=(None, 20), width='15', textvariable=FirstNameVar)
    NewFirstNameEntry.grid(row=3, column=1, padx=2, pady=2)

    Label(AddNewStaffFrame, text='Surname:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=4, column=0, padx=2, pady=2)
    SurnameVar = StringVar()
    SurnameVar.trace('w', lambda *args: limitSize(SurnameVar, 14))
    NewSurnameEntry = Entry(AddNewStaffFrame, justify='center', font=(None, 20), width='15', textvariable=SurnameVar)
    NewSurnameEntry.grid(row=4, column=1, padx=2, pady=2)

    Label(AddNewStaffFrame, text='Position:', justify='center', font=(None, 20),
          bg='#EDFBFF').grid(row=5, column=0, padx=2, pady=2)
    value = StringVar()
    NewPositionEntry = ttk.Combobox(AddNewStaffFrame, textvariable=value, state='readonly',
                                    width='14', font=(None, 20), justify='center')
    NewPositionEntry['values'] = ('Store Manager', 'Manager', 'Supervisor', 'Sales Assistant')
    NewPositionEntry.current(0)
    NewPositionEntry.grid(row=5, column=1, padx=2, pady=2)
    
    CancelButton = Button(AddNewStaffFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=ViewStaff.destroy)
    CancelButton.grid(row=6, column=0, padx=2, pady=2)
    AddNewStaffButton = Button(AddNewStaffFrame, text='Add New\nStaff', justify='center', font=(None, 18), width='10', height='4', command=lambda: add_staff_to_database(ViewStaff, NewStaffIDEntry, NewPasswordEntry, NewFirstNameEntry, NewSurnameEntry, NewPositionEntry))
    AddNewStaffButton.grid(row=6, column=1, padx=2, pady=2)

def add_staff_to_database(ViewStaff, NewStaffIDEntry, NewPasswordEntry,
                          NewFirstNameEntry, NewSurnameEntry, NewPositionEntry):
    StaffID = NewStaffIDEntry.get()
    Password = NewPasswordEntry.get()
    FirstName = NewFirstNameEntry.get()
    Surname = NewSurnameEntry.get()
    Position = NewPositionEntry.get()
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    insert_staff = '''INSERT INTO employee (staff_ID, password, fname, lname, position)
        VALUES (?, ?, ?, ?, ?);'''
    cursor.execute(insert_staff, (StaffID, Password, FirstName, Surname, Position))
    connection.commit()
    connection.close()
    ViewStaff.destroy()

def next_staff_id(NewStaffIDEntry):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(staff_ID) FROM employee')
    lastid = int(cursor.fetchone()[0])
    nextid = lastid+1
    NewStaffIDEntry.insert(0, nextid)
    connection.commit()
    connection.close()

def edit_staff(ViewStaff, ViewStaffOptionFrame):
    ViewStaff.title('View Staff - Edit Staff') #Display stock ID confirmation entry box
    ViewStaffOptionFrame.pack_forget()
    EditStaffIDFrame = Frame(ViewStaff, bg='#EDFBFF')
    EditStaffIDFrame.pack()
    Label(EditStaffIDFrame, text='EDIT STAFF', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)
    Label(EditStaffIDFrame, text='Staff ID:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=1, pady=15)
    UpdateStaffID = Entry(EditStaffIDFrame, justify='center', font=(None, 20), width=15)
    UpdateStaffID.grid(column=1, row=1, pady=15)
    UpdateStaffID.focus()
    CancelButton = Button(EditStaffIDFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4',
                          command=ViewStaff.destroy)
    CancelButton.grid(row=2, column=0, padx=2, pady=2)
    Button(EditStaffIDFrame, text='Confirm', width='10', height='4', font=(None,18),
           command=lambda: staff_id_confirmed(ViewStaff, EditStaffIDFrame, UpdateStaffID)).grid(column=1, row=2, padx=2, pady=2)

def staff_id_confirmed(ViewStaff, EditStaffIDFrame, UpdateStaffID):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    StaffID = UpdateStaffID.get()
    cursor.execute('SELECT * FROM employee WHERE staff_id=?', [StaffID])
    row = cursor.fetchone()
    if row != None:
        Password = row[1]
        FirstName = row[2]
        Surname = row[3]
        Position = row[4]
        EditStaffIDFrame.pack_forget()
        EditStaffFrame = Frame(ViewStaff, bg='#EDFBFF')
        EditStaffFrame.pack()
        Label(EditStaffFrame, text='EDIT STAFF', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)
        Label(EditStaffFrame, text='Staff ID:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=1, pady=15)
        UpdateStaffIDConfirm = Entry(EditStaffFrame, justify='center', font=(None, 20), width=15)
        UpdateStaffIDConfirm.insert(0, StaffID)
        UpdateStaffIDConfirm['state']='disabled'
        UpdateStaffIDConfirm.grid(column=1, row=1, pady=15)
        Label(EditStaffFrame, text='New Password:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=2)
        PasswordVar = StringVar()
        PasswordVar.trace('w', lambda *args: limitSize(PasswordVar, 4))
        UpdatePassword = Entry(EditStaffFrame, justify='center', font=(None, 20), width=15, show='*', textvariable=PasswordVar)
        UpdatePassword.insert(0, Password)
        UpdatePassword.grid(column=1, row=2)
        Label(EditStaffFrame, text='New First Name:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=3)
        FirstNameVar = StringVar()
        FirstNameVar.trace('w', lambda *args: limitSize(FirstNameVar, 14))
        UpdateFirstName = Entry(EditStaffFrame, justify='center', font=(None, 20), width=15, textvariable=FirstNameVar)
        UpdateFirstName.insert(0, FirstName)
        UpdateFirstName.grid(column=1, row=3)
        Label(EditStaffFrame, text='New Surname:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=4)
        SurnameVar = StringVar()
        SurnameVar.trace('w', lambda *args: limitSize(SurnameVar, 14))
        UpdateSurname = Entry(EditStaffFrame, justify='center', font=(None, 20), width=15, textvariable=SurnameVar)
        UpdateSurname.insert(0, Surname)
        UpdateSurname.grid(column=1, row=4)

        Label(EditStaffFrame, text='New Position:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=5)
        value = StringVar()
        UpdatePosition = ttk.Combobox(EditStaffFrame, textvariable=value, text=Position, state='readonly', width='14', font=(None, 20), justify='center')
        Positions = ['Store Manager', 'Manager', 'Supervisor', 'Sales Assistant']
        UpdatePosition['values'] = Positions
        UpdatePosition.current(Positions.index(Position))
        UpdatePosition.grid(column=1, row=5, padx=2, pady=2)
        
        connection.commit()
        connection.close()
        CancelButton = Button(EditStaffFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=ViewStaff.destroy)
        CancelButton.grid(row=6, column=0, padx=2, pady=2)
        UpdateStaffButton = Button(EditStaffFrame, text='Update\nStaff', justify='center', font=(None, 18), width='10', height='4', command=lambda: update_staff(ViewStaff, UpdateStaffID, UpdatePassword, UpdateFirstName, UpdateSurname, UpdatePosition))
        UpdateStaffButton.grid(row=6, column=1, padx=2, pady=2)
    
    elif row == None:
        ConfirmStaffIDError = Toplevel(bg='#EDFBFF')
        w = 200
        h = 180
        ws = ConfirmStaffIDError.winfo_screenwidth()
        hs = ConfirmStaffIDError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        ConfirmStaffIDError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ConfirmStaffIDError.title('Staff ID does NOT exist')
        Message(ConfirmStaffIDError, text='ERROR:\nStaff ID does NOT exist', justify='center', font='bold', bg='#EDFBFF').pack()
        Button(ConfirmStaffIDError, text='Try Again', font=(None, 20), width='8', height='2', command=ConfirmStaffIDError.destroy).pack(padx='10', pady='5')
        UpdateStaffID.delete(0,END)
        UpdateStaffID.focus()
        connection.commit()
        connection.close()
        edit_staff()
        
def update_staff(ViewStaff, UpdateStaffID, UpdatePassword, UpdateFirstName, UpdateSurname, UpdatePosition):
    StaffID = UpdateStaffID.get() #Get values entered in entry boxes
    Password = UpdatePassword.get()
    FirstName = UpdateFirstName.get()
    Surname = UpdateSurname.get()
    Position = UpdatePosition.get()
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Update the record with the same staff ID with new data
    cursor.execute('UPDATE employee SET password=?, fname=?, lname=?, position=? WHERE staff_ID=?',
                   (Password, FirstName, Surname, Position, StaffID))
    connection.commit()
    connection.close()
    ViewStaff.destroy()
