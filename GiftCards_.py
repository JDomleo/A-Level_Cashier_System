import datetime
import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import tabify, UpdateTotal, limitSize

def gift_card_enquiry():
    GCEnquiry = Toplevel(bg='#EDFBFF')
    w = 600 #Set up window dimensions
    h = 500 #in centre of screen
    ws = GCEnquiry.winfo_screenwidth()
    hs = GCEnquiry.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    GCEnquiry.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    GCEnquiry.title('Gift Card Enquiry')
    GCEnquiryOptionFrame = Frame(GCEnquiry, bg='#EDFBFF')
    GCEnquiryOptionFrame.pack(pady=100)
    Label(GCEnquiryOptionFrame, text='Gift Card Number:', bg='#EDFBFF', justify='center',
          font=(None, 20)).grid(row=0, column=0, padx='2', pady='5')
    GCNumVar = StringVar() #Limit entry box input size to 10 characters
    GCNumVar.trace('w', lambda *args: limitSize(GCNumVar, 10))
    GCEntry = Entry(GCEnquiryOptionFrame, justify='center', font=(None, 20), width='15',
                    textvariable=GCNumVar) #Gift card number entry box
    GCEntry.grid(row=0, column=1, padx='2', pady='5')
    GCEntry.focus()
    CancelButton = Button(GCEnquiryOptionFrame, text='Cancel', justify='center',
                          font=(None,18), width='10', height='4', command=GCEnquiry.destroy)
    CancelButton.grid(row=1, column=0, padx='2', pady='5') #Cancel button
    SearchGCButton = Button(GCEnquiryOptionFrame, text='Search', justify='center', font=(None,18),
                            width='10', height='4', command=lambda: enquiry(GCEntry, GCEnquiry))
    SearchGCButton.grid(row=1, column=1, padx='2', pady='5') #Search button

def enquiry(GCEntry, GCEnquiry):
    GCNumber = GCEntry.get() #Get gift card number entered
    GCEnquiry.destroy()
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Find gift card in database
    cursor.execute('SELECT * FROM gift_cards WHERE gift_card_number=?', [GCNumber])
    row=cursor.fetchone()
    connection.commit()
    connection.close()

    if row != None: #If gift card found
        GCFound = Toplevel(bg='#EDFBFF')
        w = 250 #Display top level window
        h = 220 #in centre of screen
        ws = GCFound.winfo_screenwidth()
        hs = GCFound.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        GCFound.geometry('%dx%d+%d+%d' % (w, h, x, y))
        IValue = row[1] #Initial gift card value
        IValue = '{:.2f}'.format(IValue)
        DatePurchased = row[2] #Date gift card purchased
        CValue = row[3] #Current gift card value
        CValue = '{:.2f}'.format(CValue) #Display gift card details to user
        Message(GCFound, bg='#EDFBFF', justify='center', width='250', font='bold',
                text=str(GCNumber)+'\n\nInitial Value: £'+str(IValue)+'\n\nDate Purchased: '
                +str(DatePurchased)+'\n\nCurrent Value: £'+str(CValue)).pack()
        OKButton = Button(GCFound, text='OK', font=(None, 20), width='8', height='2',
                          command=GCFound.destroy).pack(padx='10', pady='5')

    elif row == None: #If gift card is NOT found
        GCError = Toplevel(bg='#EDFBFF') #Display error
        w = 200 #in centre of screen
        h = 180
        ws = GCError.winfo_screenwidth()
        hs = GCError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        GCError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        GCError.title('Gift Card Does Not Exist')
        Message(GCError, bg='#EDFBFF', text='ERROR: Gift card does not exist.',
                justify='center', font='bold').pack()
        OKButton = Button(GCError, text='OK', font=(None, 20), width='8', height='2',
                          command=GCError.destroy).pack(padx='10', pady='5')
        


def gift_card_sale(TotalLabel, BarcodeEntry, ScannedItems, SignOffButton, TransVoidButton, SubtotalButton):
    GCSale = Toplevel(bg='#EDFBFF')
    w = 600 #Open top level window
    h = 500
    ws = GCSale.winfo_screenwidth()
    hs = GCSale.winfo_screenheight()
    x = (ws/2)-(w/2) #Position window in centre of screen
    y = (hs/2)-(h/2)
    GCSale.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GCSale.title('Gift Card Sale')
    
    GCSaleFrame = Frame(GCSale, bg='#EDFBFF')
    GCSaleFrame.pack(pady=100)
    
    Label(GCSaleFrame, text='Gift Card Number:', bg='#EDFBFF', justify='center',
          font=(None, 20)).grid(row=0, column=0, padx='2', pady='5')
    GCNumberEntry = Entry(GCSaleFrame, justify='center', font=(None, 20), width='15')
    GCNumberEntry.grid(row=0, column=1, padx='2', pady='5')
    next_gift_card_number(GCNumberEntry)
    GCNumberEntry['state']='disabled' #Do not allow user to change the gift card number
    
    Label(GCSaleFrame, text='Value:', bg='#EDFBFF', justify='center',
          font=(None, 20)).grid(row=1, column=0, padx='2', pady='5')
    GCValueVar = StringVar() #Limit length of input to 5 characters
    GCValueVar.trace('w', lambda *args: limitSize(GCValueVar, 5))
    GCValueEntry = Entry(GCSaleFrame, justify='center', font=(None, 20), width='15',
                         textvariable=GCValueVar) #Enter value(£) of gift card
    GCValueEntry.focus()
    GCValueEntry.grid(row=1, column=1, padx='2', pady='5')
    
    CancelButton = Button(GCSaleFrame, text='Cancel', justify='center', font=(None,18),
                          width='10', height='4', command=GCSale.destroy)
    CancelButton.grid(row=2, column=0, padx='2', pady='5')
    AddGCButton = Button(GCSaleFrame, text='Add to\nTransaction', justify='center',
                         font=(None,18), width='10', height='4',
                         command= lambda: add_gift_card(GCNumberEntry, GCValueEntry, TotalLabel, BarcodeEntry, GCSale, ScannedItems, SignOffButton, TransVoidButton, SubtotalButton))
    AddGCButton.grid(row=2, column=1, padx='2', pady='5')

def next_gift_card_number(GCNumberEntry):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM gift_cards WHERE gift_card_number=1000000001')
    exist = cursor.fetchone()
    if exist == None: #If table is empty,
        nextid = 1000000001 #make first item PK 1000000001
    else: #If table is not empty, select the last PK
        cursor.execute('SELECT MAX(gift_card_number) FROM gift_cards')
        lastid = int(cursor.fetchone()[0])
        nextid = lastid+1 #Make next ID one after the last PK
    GCNumberEntry.insert(0, nextid) #Insert nextid into GCNumberEntry
    connection.commit()
    connection.close()
    
def add_gift_card(GCNumberEntry, GCValueEntry, TotalLabel, BarcodeEntry, GCSale, ScannedItems, SignOffButton, TransVoidButton, SubtotalButton):
    minValue = 5   #Set maximum and minimum values for a gift card
    maxValue = 50
    Value = GCValueEntry.get() #Get value(£) entered for gift card
    Value = float(Value)
    if Value < minValue or Value > maxValue: #If value is too low or too high,
        GCError = Toplevel(bg='#EDFBFF') #display error
        w = 200
        h = 180
        ws = GCError.winfo_screenwidth()
        hs = GCError.winfo_screenheight()
        x = (ws/2)-(w/2) #Position error in centre of screen
        y = (hs/2)-(h/2)
        GCError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        GCError.title('Gift Card Value Out of Range')
        Message(GCError, bg='#EDFBFF', text='ERROR:\nValue out of range.\nMust be between £5 - £50.',
                justify='center', font='bold').pack()    #Allow user to try again
        TryAgainButton = Button(GCError, text='Try Again', font=(None, 20), width='8', height='2',
                                command=lambda: Try_Again_GC(GCError, GCValueEntry)).pack(padx='10', pady='5')
        
    else: #If value is within the correct range
        GCNumber = GCNumberEntry.get() #Get the next available gift card number
        Value = '{:.2f}'.format(Value)
        GCNumber = 'GC'+str(GCNumber) #Add gift card number to end of ScannedItems list
        ScannedItems.insert(END, ' '+tabify(GCNumber, 14)+tabify('Gift Card', 17)+'£'+str(Value))
        UpdateTotal(Value, True, TotalLabel) #Update total price and number of items
        GCSale.destroy() #Destroy top level window
        BarcodeEntry.focus() #Make BarcodeEntry entry box the focal point
        SignOffButton.grid_forget()
        TransVoidButton.grid(row=4, column=1, padx='10', pady='10')
        SubtotalButton.grid(row=3, column=3, padx='5', pady='2')

def Try_Again_GC(GCError, GCValueEntry):
    GCError.destroy()
    GCValueEntry.delete(0, 'end')
