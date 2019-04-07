import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import tabify, limitSize

def view_stock():
    ViewStock = Toplevel(bg='#EDFBFF')
    w = 600
    h = 500
    ws = ViewStock.winfo_screenwidth()
    hs = ViewStock.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    ViewStock.geometry('%dx%d+%d+%d' % (w, h, x, y))
    ViewStock.title('View Stock')
    ViewStockOptionFrame = Frame(ViewStock, bg='#EDFBFF')
    ViewStockOptionFrame.pack(pady=100)
    DisplayStockButton = Button(ViewStockOptionFrame, text='Display\nStock', width='18', height='7', command=lambda: display_stock(ViewStock, ViewStockOptionFrame))
    DisplayStockButton.grid(column=0, row=0, padx=20,)
    AddStockButton = Button(ViewStockOptionFrame, text='Add\nStock', width='18', height='7', command=lambda: add_stock_button(ViewStock, ViewStockOptionFrame))
    AddStockButton.grid(column=1, row=0, padx=20)
    EditStockButton = Button(ViewStockOptionFrame, text='Edit\nStock', width='18', height='7', command=lambda: edit_stock(ViewStock, ViewStockOptionFrame))
    EditStockButton.grid(column=2, row=0, padx=20)
    CancelButton = Button(ViewStockOptionFrame, text='Cancel', justify='center', width='18', height='7', command=ViewStock.destroy)
    CancelButton.grid(column=1, row=1, pady=20)

def display_stock(ViewStock, ViewStockOptionFrame):
    ViewStock.title('View Stock - Display Stock')
    ViewStockOptionFrame.pack_forget()
    DisplayStockFrame = Frame(ViewStock, bg='#EDFBFF')
    DisplayStockFrame.pack()
    global StockCanvas
    StockCanvas = Canvas(DisplayStockFrame, width='560', height='490', bg='#EDFBFF', highlightthickness=0)
    StockCanvas.pack(side=LEFT)
    StockGridFrame = Frame(StockCanvas, bg='#EDFBFF')
    StockGridFrame.pack()
    nextrow=0
    Label(StockGridFrame, text='Stock_ID', bg='#EDFBFF', font='bold').grid(column=0, row=nextrow, padx='20', pady='5')
    Label(StockGridFrame, text='Item_Name', bg='#EDFBFF', font='bold').grid(column=1, row=nextrow, padx='20', pady='5')
    Label(StockGridFrame, text='Unit_Price', bg='#EDFBFF', font='bold').grid(column=2, row=nextrow, padx='20', pady='5')
    Label(StockGridFrame, text='No_in_Stock', bg='#EDFBFF', font='bold').grid(column=3, row=nextrow, padx='20', pady='5')
    nextrow=nextrow+1
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM stock')
    AllStock = cursor.fetchall()
    for row in AllStock:
        Label(StockGridFrame, text=row[0], bg='#EDFBFF').grid(column=0, row=nextrow, padx='20')
        Label(StockGridFrame, text=row[1], bg='#EDFBFF').grid(column=1, row=nextrow, padx='20')
        Price = '{:.2f}'.format(row[2])
        Label(StockGridFrame, text='£'+str(Price),
              bg='#EDFBFF').grid(column=2, row=nextrow, padx='20')
        Label(StockGridFrame, text=row[3], bg='#EDFBFF').grid(column=3, row=nextrow, padx='20')
        nextrow=nextrow+1
    connection.commit()
    connection.close()
    CancelButton = Button(StockGridFrame, text='Cancel', justify='center', width='10', height='4', command=ViewStock.destroy)
    CancelButton.grid(row=nextrow, column=1, columnspan=2)
    StockScrollbar = Scrollbar(DisplayStockFrame, orient="vertical")
    StockScrollbar.pack(side=RIGHT, fill=Y)
    StockCanvas.config(yscrollcommand=StockScrollbar.set)
    StockScrollbar.config(command=StockCanvas.yview)
    StockCanvas.create_window((0,0),window=StockGridFrame)
    StockGridFrame.bind("<Configure>",StockCanvasScroll)

def StockCanvasScroll(event):
    StockCanvas.configure(scrollregion=StockCanvas.bbox("all"))

def add_stock_button(ViewStock, ViewStockOptionFrame):
    ViewStock.title('View Stock - Add Stock')
    ViewStockOptionFrame.pack_forget()
    AddNewStockFrame = Frame(ViewStock, bg='#EDFBFF')
    AddNewStockFrame.pack(pady=50)
    Label(AddNewStockFrame, text='ADD STOCK', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)

    Label(AddNewStockFrame, text='Stock ID:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=1, column=0, padx=2, pady=2)
    NewStockIDEntry = Entry(AddNewStockFrame, justify='center', font=(None, 20), width='15')
    NewStockIDEntry.grid(row=1, column=1, padx=2, pady=2)
    next_stock_id(NewStockIDEntry)
    NewStockIDEntry['state']='disabled'

    Label(AddNewStockFrame, text='Item Name:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=2, column=0, padx=2, pady=2)
    ItemNameVar = StringVar()
    ItemNameVar.trace('w', lambda *args: limitSize(ItemNameVar, 14))
    NewItemNameEntry = Entry(AddNewStockFrame, justify='center', font=(None, 20), width='15', textvariable=ItemNameVar)
    NewItemNameEntry.grid(row=2, column=1, padx=2, pady=2)
    NewItemNameEntry.focus()

    Label(AddNewStockFrame, text='Unit_Price: £', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=3, column=0, padx=2, pady=2)
    UnitPriceVar = StringVar()
    UnitPriceVar.trace('w', lambda *args: limitSize(UnitPriceVar, 5))
    NewUnitPriceEntry = Entry(AddNewStockFrame, justify='center', font=(None, 20), width='15', textvariable=UnitPriceVar)
    NewUnitPriceEntry.grid(row=3, column=1, padx=2, pady=2)

    Label(AddNewStockFrame, text='No_in_Stock:', justify='center', font=(None, 20), bg='#EDFBFF').grid(row=4, column=0, padx=2, pady=2)
    NoinStockVar = StringVar()
    NoinStockVar.trace('w', lambda *args: limitSize(NoinStockVar, 6))
    NewNoinStockEntry = Entry(AddNewStockFrame, justify='center', font=(None, 20), width='15', textvariable=NoinStockVar)
    NewNoinStockEntry.grid(row=4, column=1, padx=2, pady=2)
    
    CancelButton = Button(AddNewStockFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=ViewStock.destroy)
    CancelButton.grid(row=5, column=0, padx=2, pady=2)
    AddNewStockButton = Button(AddNewStockFrame, text='Add New\nStock', justify='center', font=(None, 18), width='10', height='4', command=lambda: add_stock_to_database(ViewStock, NewStockIDEntry, NewItemNameEntry, NewUnitPriceEntry, NewNoinStockEntry))
    AddNewStockButton.grid(row=5, column=1, padx=2, pady=2)

def add_stock_to_database(ViewStock, NewStockIDEntry, NewItemNameEntry, NewUnitPriceEntry, NewNoinStockEntry):
    StockID = NewStockIDEntry.get()
    ItemName = NewItemNameEntry.get()
    UnitPrice = NewUnitPriceEntry.get()
    NoinStock = NewNoinStockEntry.get()
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    insert_stock = '''INSERT INTO stock (stock_ID, item_name, unit_price, no_in_stock)
        VALUES (?, ?, ?, ?);'''
    cursor.execute(insert_stock, (StockID, ItemName, UnitPrice, NoinStock))
    connection.commit()
    connection.close()
    ViewStock.destroy()

def next_stock_id(NewStockIDEntry):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM stock WHERE stock_id=100000000001')
    exist = cursor.fetchone()
    if exist == None:
        nextid = 100000000001
    else:
        cursor.execute('SELECT MAX(stock_ID) FROM stock')
        lastid = int(cursor.fetchone()[0])
        nextid = lastid+1
    NewStockIDEntry.insert(0, nextid)
    connection.commit()
    connection.close()

def edit_stock(ViewStock, ViewStockOptionFrame):
    ViewStock.title('View Stock - Edit Stock')
    ViewStockOptionFrame.pack_forget()
    EditStockIDFrame = Frame(ViewStock, bg='#EDFBFF')
    EditStockIDFrame.pack()
    Label(EditStockIDFrame, text='EDIT STOCK', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)
    Label(EditStockIDFrame, text='Stock ID:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=1, pady=15)
    UpdateStockID = Entry(EditStockIDFrame, justify='center', font=(None, 20), width=15)
    UpdateStockID.grid(column=1, row=1, pady=15)
    UpdateStockID.focus()
    CancelButton = Button(EditStockIDFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=ViewStock.destroy)
    CancelButton.grid(row=2, column=0, padx=2, pady=2)
    Button(EditStockIDFrame, text='Confirm', width='10', height='4', font=(None,18), command=lambda: stock_id_confirmed(ViewStock, EditStockIDFrame, UpdateStockID)).grid(column=1, row=2, padx=2, pady=2)

def stock_id_confirmed(ViewStock, EditStockIDFrame, UpdateStockID):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    StockID = UpdateStockID.get()
    cursor.execute('SELECT * FROM stock WHERE stock_id=?', [StockID])
    row = cursor.fetchone()
    if row != None:
        ItemName = row[1]
        UnitPrice = '{:.2f}'.format(row[2])
        NoinStock = row[3]
        EditStockIDFrame.pack_forget()
        EditStockFrame = Frame(ViewStock, bg='#EDFBFF')
        EditStockFrame.pack()
        Label(EditStockFrame, text='EDIT STOCK', font='bold', bg='#EDFBFF').grid(column=0, row=0, columnspan=2)
        Label(EditStockFrame, text='Stock ID:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=1, pady=15)
        UpdateStockIDConfirm = Entry(EditStockFrame, justify='center', font=(None, 20), width=15)
        UpdateStockIDConfirm.insert(0, StockID)
        UpdateStockIDConfirm['state']='disabled'
        UpdateStockIDConfirm.grid(column=1, row=1, pady=15)
        Label(EditStockFrame, text='New Item Name:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=2)
        ItemNameVar = StringVar()
        ItemNameVar.trace('w', lambda *args: limitSize(ItemNameVar, 14))
        UpdateItemName = Entry(EditStockFrame, justify='center', font=(None, 20), width=15, textvariable=ItemNameVar)
        UpdateItemName.insert(0, ItemName)
        UpdateItemName.grid(column=1, row=2)
        Label(EditStockFrame, text='New Unit Price: £', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=3)
        UnitPriceVar = StringVar()
        UnitPriceVar.trace('w', lambda *args: limitSize(UnitPriceVar, 5))
        UpdateUnitPrice = Entry(EditStockFrame, justify='center', font=(None, 20), width=15, textvariable=UnitPriceVar)
        UpdateUnitPrice.insert(0, UnitPrice)
        UpdateUnitPrice.grid(column=1, row=3)
        Label(EditStockFrame, text='New No. in Stock:', justify='center', font=(None, 20), bg='#EDFBFF').grid(column=0, row=4)
        NoinStockVar = StringVar()
        NoinStockVar.trace('w', lambda *args: limitSize(NoinStockVar, 6))
        UpdateNoinStock = Entry(EditStockFrame, justify='center', font=(None, 20), width=15, textvariable=NoinStockVar)
        UpdateNoinStock.insert(0, NoinStock)
        UpdateNoinStock.grid(column=1, row=4)
        
        connection.commit()
        connection.close()
        CancelButton = Button(EditStockFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=ViewStock.destroy)
        CancelButton.grid(row=5, column=0, padx=2, pady=2)
        UpdateStockButton = Button(EditStockFrame, text='Update\nStock', justify='center', font=(None, 18), width='10', height='4', command=lambda: update_stock(ViewStock, UpdateStockID, UpdateItemName, UpdateUnitPrice, UpdateNoinStock))
        UpdateStockButton.grid(row=5, column=1, padx=2, pady=2)
    
    elif row == None: #If row not found in database
        ConfirmStockIDError = Toplevel(bg='#EDFBFF')
        w = 200 #Create top level window
        h = 180 #in centre of screen.
        ws = ConfirmStockIDError.winfo_screenwidth()
        hs = ConfirmStockIDError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        ConfirmStockIDError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        ConfirmStockIDError.title('Staff ID does NOT exist') #Window title
        Message(ConfirmStockIDError, text='ERROR:\nStock ID does NOT exist', justify='center',
                font='bold', bg='#EDFBFF').pack() #Error message
        Button(ConfirmStockIDError, text='Try Again', font=(None, 20), width='8', height='2',
               command=ConfirmStockIDError.destroy).pack(padx='10', pady='5') #Try again
        UpdateStockID.delete(0,END) #Clear stock ID entry box
        UpdateStockID.focus() #Focus stock ID entry box
        connection.commit()
        connection.close() #Re-run edit_stock function
        
def update_stock(ViewStock, UpdateStockID, UpdateItemName, UpdateUnitPrice, UpdateNoinStock):
    StockID = UpdateStockID.get()
    ItemName = UpdateItemName.get()
    UnitPrice = UpdateUnitPrice.get()
    NoinStock = UpdateNoinStock.get()
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE stock SET item_name=?, unit_price=?, no_in_stock=? WHERE stock_id=?', (ItemName, UnitPrice, NoinStock, StockID))
    connection.commit()
    connection.close()
    ViewStock.destroy()
