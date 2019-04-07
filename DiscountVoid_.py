import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import tabify, UpdateTotal

def Discount(TotalLabel, ScannedItems, BarcodeEntry):
    focus = ScannedItems.curselection()
    line = ScannedItems.get(focus)
    if line[1:3] == 'GC': #If selected item is gift card
        GCDiscount = Toplevel(bg='#EDFBFF')
        w = 200 #Open top-level window
        h = 180 #in centre of screen
        ws = GCDiscount.winfo_screenwidth()
        hs = GCDiscount.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        GCDiscount.geometry('%dx%d+%d+%d' % (w, h, x, y))
        GCDiscount.title('Gift Card Discount')
        Message(GCDiscount, bg='#EDFBFF', text='ERROR:\nA gift card cannot be discounted.',
                justify='center', font='bold').pack() #Error message
        OKButton = Button(GCDiscount, text='OK', font=(None, 20), width='8', height='2',
                          command=GCDiscount.destroy).pack(padx='10', pady='5')
    else:
        try:
            DiscountWindow = Toplevel(bg='#EDFBFF')
            w = 600 #Open discount top level window
            h = 500 #in centre of screen.
            ws = DiscountWindow.winfo_screenwidth()
            hs = DiscountWindow.winfo_screenheight()
            x = (ws/2)-(w/2)
            y = (hs/2)-(h/2)
            DiscountWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
            DiscountWindow.title('Discount')
            
            DiscountOptionFrame = Frame(DiscountWindow, bg='#EDFBFF')
            DiscountOptionFrame.pack(pady=100)
            Label(DiscountOptionFrame, text='Discount Percentage: ', font=(None, 20),
                  bg='#EDFBFF').grid(column=0, row=0, padx=5)
            PercentageSpinbox = Spinbox(DiscountOptionFrame, from_=0, to=100,
                                        font=(None, 20), width=3, state='readonly')
            PercentageSpinbox.grid(column=1, row=0) #Display spinbox (0-100)
            Label(DiscountOptionFrame, text='%', font=(None, 20),
                  bg='#EDFBFF').grid(column=2, row=0) #Apply discount button
            Button(DiscountOptionFrame, text='Apply\nDiscount', justify='center',
                   font=(None,18), width='10', height='4',
                   command=lambda: apply_discount(TotalLabel, ScannedItems, BarcodeEntry,
                                                  DiscountWindow, PercentageSpinbox, focus,
                                                  line)).grid(column=0, row=1, columnspan=2, pady=10)
        except TclError:
            DiscountError = Toplevel(bg='#EDFBFF')
            w = 400
            h = 300
            ws = DiscountError.winfo_screenwidth()
            hs = DiscountError.winfo_screenheight()
            x = (ws/2)-(w/2)
            y = (hs/2)-(h/2)
            DiscountError.geometry('%dx%d+%d+%d' % (w, h, x, y))
            DiscountError.title('Discount Error')
            Message(DiscountError, text='ERROR: You must select an item to discount.', justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
            Button(DiscountError, text='Ok', justify='center', font=(None,18), width='10', height='4', command=DiscountError.destroy).pack()

def apply_discount(TotalLabel, ScannedItems, BarcodeEntry, DiscountWindow,
                   PercentageSpinbox, focus, line):
    StockID = line[1:13] #Get stock ID from selected item
    DiscountPercent = int(PercentageSpinbox.get()) #Get percentage
    DiscountValue = float(1-(DiscountPercent/100)) #Convert percentage
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Get item's original price
    cursor.execute('SELECT * FROM stock WHERE stock_id=?', [StockID])
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    DiscountPrice = row[2] * DiscountValue #Calculate discounted price
    DiscountPrice = '{:.2f}'.format(DiscountPrice)
    PriceDifference = (float(row[2]) - float(DiscountPrice)) #Price difference
    ScannedItems.delete(focus) #Replace selected line with new price
    ScannedItems.insert(focus, ' '+tabify(str(row[0]), 14)+tabify(str(row[1]), 17)
                        +'£'+str(DiscountPrice)+' (-'+str(DiscountPercent)+'%)')
    UpdateTotal(PriceDifference, 'discount', TotalLabel) #Update total price
    DiscountWindow.destroy()
    BarcodeEntry.focus()

def Void(TotalLabel, ScannedItems, BarcodeEntry):
    try: #If an item has been selected
        focus = ScannedItems.curselection() #Get selected index
        line = ScannedItems.get(focus) #Get selected line
        price = float(line[33:len(line)])
        UpdateTotal(price, 'void', TotalLabel) #Update the total price
        ScannedItems.delete(focus) #Remove selected line from list box
        
    except TclError: #If NO item is selected
        VoidError = Toplevel(bg='#EDFBFF')
        w = 400
        h = 300
        ws = VoidError.winfo_screenwidth()
        hs = VoidError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2) #Show error message in centre of screen
        VoidError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        VoidError.title('Void Error')
        Message(VoidError, text='ERROR: You must select an item to void.', justify='center',
                font=(None, 18), bg='#EDFBFF', width='250').pack()
        Button(VoidError, text='Ok', justify='center', font=(None,18), width='10', height='4',
               command=VoidError.destroy).pack()
        
    BarcodeEntry.focus()

