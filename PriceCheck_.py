import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import tabify, UpdateTotal, limitSize

def price_check(TotalLabel, ScannedItems, BarcodeEntry):
    PriceCheck = Toplevel(bg='#EDFBFF')
    w = 600 #Open top level window in the centre of the computer's screen
    h = 500
    ws = PriceCheck.winfo_screenwidth()
    hs = PriceCheck.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    PriceCheck.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    PriceCheck.title('Price Check')
    PriceCheckFrame = Frame(PriceCheck, bg='#EDFBFF')
    PriceCheckFrame.pack(pady=100)
    
    Label(PriceCheckFrame, text='Barcode :', justify='center', font=(None, 20),
          bg='#EDFBFF').grid(row=0, column=0, padx=2, pady=2)
    BarcodeVar = StringVar() #Search database by barcode reference
    BarcodeVar.trace('w', lambda *args: limitSize(BarcodeVar, 12))
    BarcodeSearch = Entry(PriceCheckFrame, justify='center', font=(None, 20), width='15', textvariable=BarcodeVar)
    BarcodeSearch.grid(row=0, column=1, padx=2, pady=2)
    BarcodeSearch.focus()
    
    Label(PriceCheckFrame, text='Item Description :', justify='center',
          font=(None, 20), bg='#EDFBFF').grid(row=1, column=0, padx=2, pady=2)
    DescriptionVar = StringVar() #Search database by item name reference
    DescriptionVar.trace('w', lambda *args: limitSize(DescriptionVar, 14))
    DescriptionSearch = Entry(PriceCheckFrame, justify='center', font=(None, 20), width='15', textvariable=DescriptionVar)
    DescriptionSearch.grid(row=1, column=1, padx=2, pady=2)
    
    Button(PriceCheckFrame, text='Search', justify='center', font=(None,18),width='10', height='4', #Search button
           command=lambda: search_item(TotalLabel, ScannedItems, BarcodeEntry, PriceCheck, PriceCheckFrame,
                                       BarcodeSearch, DescriptionSearch)).grid(row=2, column=0, columnspan=2, pady=2)

def search_item(TotalLabel, ScannedItems, BarcodeEntry, PriceCheck, PriceCheckFrame, BarcodeSearch, DescriptionSearch):
    Barcode = BarcodeSearch.get()
    Description = DescriptionSearch.get() #Display relevant widgets needed to show searched items
    PriceCheckFrame.pack_forget()
    SearchFrame= Frame(PriceCheck, bg='#EDFBFF')
    SearchFrame.pack(padx=2, pady=5)
    Label(SearchFrame, bg='#EDFBFF', font='bold', text='Items Matched').grid(row=0, column=0, columnspan=2)
    Label(SearchFrame, font = 'Courier', bg='#FFFFFF', width='46',
          text='  '+tabify('Stock ID', 14)+tabify('Item Name', 17)+'Price', anchor='w').grid(row=1, column=0, columnspan=2)

    ListboxFrame = Frame(SearchFrame) #Set up list box ready to show found items
    ListboxFrame.configure(width='45', bg='#EDFBFF')
    SearchedItems = Listbox(ListboxFrame, font = 'Courier')
    SearchedItems.config(width='45', height='15')
    SearchedItems.pack(side=LEFT)
    SearchScrollbar = Scrollbar(ListboxFrame) #Include scrollbar in case list is longer than space given
    SearchScrollbar.pack(side=RIGHT, fill=Y)
    SearchedItems.config(yscrollcommand=SearchScrollbar.set)
    SearchScrollbar.config(command=SearchedItems.yview)
    ListboxFrame.grid(row=2, column=0, columnspan=2)

    Button(SearchFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4',
           command=PriceCheck.destroy).grid(row=3, column=0, pady=2) #Cancel button - close window
    #Add item to window button
    Button(SearchFrame, text='Add Item to\nTransaction', justify='center', font=(None,18), width='10', height='4',
           command=lambda: add_search_to_transaction(TotalLabel, ScannedItems, BarcodeEntry, PriceCheck,
                                                     SearchedItems)).grid(row=3, column=1, pady=2)
    
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Search stock table by barcode or/and item name
    cursor.execute('SELECT * FROM stock WHERE stock_id=? OR item_name=?', [Barcode, Description])
    Searched = cursor.fetchall() #Store all matched rows as an array called 'Searched'
    for row in Searched: #For every row in 'Searched' array, display barcode, item name and price
        price = '{:.2f}'.format(row[2])
        SearchedItems.insert(END, ' '+tabify(str(row[0]), 14)+tabify(str(row[1]), 17)+'£'+str(price))
    connection.commit()
    connection.close()

def add_search_to_transaction(TotalLabel, ScannedItems, BarcodeEntry, PriceCheck, SearchedItems):
    try: #If an item has been selected
        SearchFocus = SearchedItems.curselection()
        item = SearchedItems.get(SearchFocus)
        ScannedItems.insert(END, item)
        PriceCheck.destroy()
        BarcodeEntry.focus()
        price = float(item[33:len(item)]) #Retrieve price from string
        UpdateTotal(price, True, TotalLabel)

    except TclError: #If NO item has been selected
        AddSearchError = Toplevel(bg='#EDFBFF')
        w = 400
        h = 300
        ws = AddSearchError.winfo_screenwidth()
        hs = AddSearchError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        AddSearchError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        AddSearchError.title('Add Search Item Error') #Display error
        Message(AddSearchError, text='ERROR: You must select an item to add to the transaction.',
                justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
        Button(AddSearchError, text='Ok', justify='center', font=(None,18), width='10',
               height='4', command=AddSearchError.destroy).pack()
