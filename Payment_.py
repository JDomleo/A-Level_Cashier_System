import datetime
import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import *

def payment(value, TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry):
    TotalPrice = TotalPricePayLabel['text'] #Get total price
    if 'Remaining' in TotalPrice:
        Start = 18
    else:
        Start = 8
    TotalPrice = TotalPrice[Start:len(TotalPrice)]
    TotalPrice = float(TotalPrice)
    if value == 'Exact Cash': #Exact Cash button clicked?
        value = TotalPrice
    elif value == 'Cash': #Cash button clicked?
        value = CashEntry.get()
    value = float(value)
    if value < TotalPrice:
        CashError = Toplevel(bg='#EDFBFF')
        w = 200 #Display cash error
        h = 180 #Not enough cash given
        ws = CashError.winfo_screenwidth()
        hs = CashError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        CashError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        CashError.title('Cash Value Insufficent')
        Message(CashError, bg='#EDFBFF', text='ERROR:\nCash is too low.\nEnter a higher value.',
                justify='center', font='bold').pack()
        OKButton = Button(CashError, text='OK', font=(None, 20), width='8', height='2',
                          command=CashError.destroy).pack(padx='10', pady='5')
        ChangeDueLabel['text']='Change Due:' #Reset labels
        CashPaidLabel['text']='Cash Paid:'
    else:
        ChangeDue = abs(float(TotalPrice) - float(value)) #Change due = difference
        ChangeDue = '{:.2f}'.format(ChangeDue) #Display change due
        value = '{:.2f}'.format(value)
        ChangeDueLabel['text']='Change Due: £'+str(ChangeDue)
        CashPaidLabel['text']='Cash Paid: £'+str(value) #Display cash paid
    CashEntry.delete(0, END)

    

def GCPayment(TotalPricePayLabel, CashPaidLabel, ChangeDueLabel):
    GCPay = Toplevel(bg='#EDFBFF')
    w = 600
    h = 500
    ws = GCPay.winfo_screenwidth()
    hs = GCPay.winfo_screenheight()
    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)
    GCPay.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GCPay.title('Gift Card Payment')
    GCPayFrame = Frame(GCPay, bg='#EDFBFF')
    GCPayFrame.pack(pady='80')
    GCNumVar = StringVar()
    GCNumVar.trace('w', lambda *args: limitSize(GCNumVar, 10))
    GCNumberEntry = Entry(GCPayFrame, justify='center', font=(None, 20), width='15', textvariable=GCNumVar)
    GCNumberEntry.grid(row=0, column=0, columnspan=2, padx='2', pady='5')
    GCNumberEntry.focus()
    CancelButton = Button(GCPayFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=GCPay.destroy)
    CancelButton.grid(row=1, column=0, padx='5', pady='5')
    ConfirmGCButton = Button(GCPayFrame, text='Confirm', justify='center', font=(None,18), width='10', height='4', command=lambda: GCPaymentConfirm(GCPay, GCNumberEntry, GCPayFrame, TotalPricePayLabel, CashPaidLabel, ChangeDueLabel))
    ConfirmGCButton.grid(row=1, column=1, padx='5', pady='5')

def GCPaymentConfirm(GCPay, GCNumberEntry, GCPayFrame, TotalPricePayLabel,
                     CashPaidLabel, ChangeDueLabel):
    TotalPrice = TotalPricePayLabel['text'] #Get total price
    if 'Remaining' in TotalPrice:
        Start = 18
    else:
        Start = 8
    TotalPrice = TotalPrice[Start:len(TotalPrice)]
    GCNumber = GCNumberEntry.get() #Get gift card number
    GCPayFrame.pack_forget()
    GCConfirmFrame = Frame(GCPay, bg='#EDFBFF')
    GCConfirmFrame.pack(pady='60')
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Search database for gift card
    cursor.execute('SELECT * FROM gift_cards WHERE gift_card_number=?', [GCNumber])
    row=cursor.fetchone()
    connection.commit()
    connection.close()
    if row[3] > 0: #If gift card NOT empty
        CurrentValue = row[3]
        NewTotal = float(TotalPrice)-float(CurrentValue)
        if NewTotal < 0: #Has gift card paid all of total price?
            NewCurrentValue = abs(NewTotal) #Current value = extra paid
            AmountPaid = float(CurrentValue) - float(NewCurrentValue) #Difference
            NewCurrentValue = '{:.2f}'.format(NewCurrentValue)
            NewTotal=0 #Remaining total = £0.00
        else:
            NewCurrentValue = '0.00' #Gift card has been maxed out
            AmountPaid=float(CurrentValue) #Amount paid = gift card's value
        NewTotal = '{:.2f}'.format(NewTotal)
        AmountPaid = '{:.2f}'.format(AmountPaid)
        IValue = '{:.2f}'.format(row[1])
        Label(GCConfirmFrame, text='Gift Card Number: ', bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=0, column=0, padx='2', pady='5')
        Label(GCConfirmFrame, text=str(GCNumber), bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=0, column=1, padx='2', pady='5')
        Label(GCConfirmFrame, text='Initial Value: ', bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=1, column=0, padx='2', pady='5')
        Label(GCConfirmFrame, text='£'+str(IValue), bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=1, column=1, padx='2', pady='5')
        Label(GCConfirmFrame, text='Remaining Total: ', bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=2, column=0, padx='2', pady='5')
        Label(GCConfirmFrame, text='£'+str(NewTotal), bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=2, column=1, padx='2', pady='5')
        Label(GCConfirmFrame, text='Amount Paid: ', bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=3, column=0, padx='2', pady='5')
        Label(GCConfirmFrame, text='£'+str(AmountPaid), bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=3, column=1, padx='2', pady='5')
        Label(GCConfirmFrame, text='New Gift Card Balance: ', bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=4, column=0, padx='2', pady='5')
        Label(GCConfirmFrame, text='£'+str(NewCurrentValue), bg='#EDFBFF', justify='center', font=(None, 20)).grid(row=4, column=1, padx='2', pady='5')
        CancelButton = Button(GCConfirmFrame, text='Cancel', justify='center', font=(None,18), width='10', height='4', command=GCPay.destroy)
        CancelButton.grid(row=5, column=0, padx='5', pady='5')
        PayGC = Button(GCConfirmFrame, text='Use This\nGift Card', justify='center', font=(None,18), width='10', height='4', command=lambda: pay_gift_card(NewTotal, NewCurrentValue, GCPay, GCNumber, AmountPaid, TotalPricePayLabel, CashPaidLabel, ChangeDueLabel))
        PayGC.grid(row=5, column=1, padx='5', pady='5')
    else:
        GCError = Toplevel(bg='#EDFBFF')
        w = 200
        h = 180
        ws = GCError.winfo_screenwidth()
        hs = GCError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        GCError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        GCError.title('Gift Card Value Insufficent')
        Message(GCError, bg='#EDFBFF', text='ERROR:\nGift card value is empty. Try a different payment method.', justify='center', font='bold').pack()
        OKButton = Button(GCError, text='OK', font=(None, 20), width='8', height='2', command=GCError.destroy).pack(padx='10', pady='5')
        GCPay.destroy()


def pay_gift_card(NewTotal, NewCurrentValue, GCPay, GCNumber, AmountPaid, TotalPricePayLabel, CashPaidLabel, ChangeDueLabel):
    TotalPricePayLabel['text']='Remaining Total: £'+str(NewTotal)
    CashPaidLabel['text']='Cash Paid: £0.00' #Update payment labels
    ChangeDueLabel['text']='Change Due: £0.00'
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Update gift card current value
    cursor.execute('UPDATE gift_cards SET current_value=? WHERE gift_card_number=?', [NewCurrentValue, GCNumber])
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS temp_GC_transaction (
    gift_card_number INTEGER,
    amount_paid REAL);''') #Create temporary table
    insert_temp='''INSERT INTO temp_GC_transaction (gift_card_number, amount_paid)
                   VALUES (?, ?);'''
    cursor.execute(insert_temp, (GCNumber, AmountPaid)) #Temporary store GCNum & AmountPaid
    connection.commit()
    connection.close()
    GCPay.destroy()
    EasyAccess = [1, 5, 10, 20]
    TextPound=[OnePoundButton, FivePoundButton, TenPoundButton, TwentyPoundButton]
    for i in range(0, len(EasyAccess)):
        if float(EasyAccess[i]) >= float(NewTotal):
            DisableButton = TextPound[i]
            DisableButton['state']='normal'
        elif EasyAccess[i] < float(NewTotal):
            break


def complete_transaction(CashPaidLabel, ChangeDueLabel, StaffNumberLabel, ScannedItems, TransVoidButton, SignOffButton, TotalLabel, Return_to_Selling, Return_to_Refund, cancel_refund, root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, TransIDLabel, EnterBarcodeLabel, BarcodeEntry, RefundItems, FuncFrame):
    transactionID = next_transaction_id()
    TotalPrice = UpdateTotal(0, 'Get Total Price', 0)
    if float(TotalPrice) < 0:
        isRefund = True
    else:
        isRefund = False
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    try: #Check if temporary table exists
        cursor.execute('SELECT * FROM temp_GC_transaction')
        GiftCardsUsed=cursor.fetchall()
        for row in GiftCardsUsed: #For each gift card used to pay with
            GCNumber = row[0]
            AmountPaid = row[1]
            insert_GCtrans = '''INSERT INTO gift_card_transaction (gift_card_number, transaction_id, Gift_Card_Value_Paid)
                Values(?, ?, ?);''' #Insert data into link table
            cursor.execute(insert_GCtrans, (GCNumber, transactionID, AmountPaid))
        cursor.execute('DROP TABLE temp_GC_transaction') #Delete temporary table
        GiftCardUsed = True
    except sqlite3.OperationalError: #If table could not be open: doesn't exist
        GiftCardUsed = False #Therefore, gift card hasn't been used to pay with
    CashPaid = CashPaidLabel['text']
    CashPaid = CashPaid[12:len(CashPaid)]
    CashPaid = float(CashPaid)
    CashPaid = '{:.2f}'.format(CashPaid)
    ChangeDue = ChangeDueLabel['text']
    ChangeDue = ChangeDue[13:len(ChangeDue)]
    ChangeDue = float(ChangeDue)
    ChangeDue = '{:.2f}'.format(ChangeDue)
    NoofItems = UpdateTotal(0, 'Get NoofItems', 0)
    StaffID = StaffNumberLabel['text']
    StaffID = StaffID[10:len(StaffID)]
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().strftime('%H:%M:%S')
    items=[]
    quantity=[]
    GiftCards=[]
    GiftCardValue=[]
    GetItems(items, quantity, GiftCards, GiftCardValue, ScannedItems)
    insert_transaction = '''INSERT INTO transactions (transaction_id, staff_ID, date, time, Total_Price,
                            No_of_Items, Cash_Paid, Change_Due, Gift_Card_Used, is_Refund)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''' #Summarise transaction by inserting data into database
    cursor.execute(insert_transaction, (transactionID, StaffID, Date, Time, TotalPrice, NoofItems,
                                        CashPaid, ChangeDue, GiftCardUsed, isRefund))
    
    #Stock control
    for i in range(0, len(items)):
        StockID = items[i] #For each product bought
        Quantity = quantity[i] #Alter stock number by quantity
        cursor.execute('SELECT * FROM stock WHERE stock_id=?', [StockID])
        row = cursor.fetchone()
        if isRefund == False: #If NOT refund, subtract stock
            NoinStock = row[3]-Quantity
            unit_price = row[2]
        elif isRefund == True: #If refund, add stock
            NoinStock = row[3]+Quantity
            unit_price = 0 - float(row[2])
        cursor.execute('UPDATE stock SET no_in_stock=? WHERE stock_id=?', [NoinStock, StockID])
        Price = Quantity * unit_price #Update database with new stock values
        Price = '{:.2f}'.format(Price)
        insert_transaction_stock = '''INSERT INTO transaction_stock (transaction_id, stock_id, quantity, quan_price)
            VALUES (?, ?, ?, ?);''' #Insert stock data into link table
        cursor.execute(insert_transaction_stock, (transactionID, StockID, Quantity, Price))

    #Gift Card Sale
    for j in range(0, len(GiftCards)): #For each gift card purchased
        GCNumber = GiftCards[j]
        GCNumber = GCNumber[2:len(GCNumber)]
        Value = GiftCardValue[j]
        Date = datetime.date.today().strftime('%d/%m/%Y') #Get the date (DD/MM/YYYY)
        insert_GC = '''INSERT INTO gift_cards (gift_card_number, initial_value, date_purchased, current_value)
                       VALUES (?, ?, ?, ?)'''
        #Insert the GCNumber, inital value, date purchased and current value into gift_cards table
        cursor.execute(insert_GC, (GCNumber, Value, Date, Value))
        GCNumber = 'GC' + str(GCNumber)
        insert_transaction_stock = '''INSERT INTO transaction_stock (transaction_id, stock_id, quantity, quan_price)
            VALUES (?, ?, ?, ?);''' #Insert gift card data into link table
        cursor.execute(insert_transaction_stock, (transactionID, GCNumber, '1', Value))

    Date = datetime.date.today().strftime('%d/%m/%Y')
    #Create receipt
    ReceiptFile = 'Receipts\Receipt'+str(transactionID)
    receipt = open(ReceiptFile, 'w+') #Create new file in 'Receipts' folder
    ReceiptList = 'Jenny\'s Gift Shop\n' #Begin receipt message
    for r in range(0, len(items)): #List items bought on receipt
        StockID = items[r]
        Quantity = quantity[r]
        cursor.execute('SELECT * FROM stock WHERE stock_id=?', [StockID])
        row = cursor.fetchone()
        for x in range(0, Quantity): #Display item's quantity
            ReceiptList = ReceiptList+'\n'+str(row[1])+'\t£'+str(row[2])
    for g in range(0, len(GiftCards)): #List gift card sales
        ReceiptList = ReceiptList+'\nGift Card\t£'+str(GiftCardValue[g])
    #Display receipt message and other important information
    ReceiptList = ReceiptList+'\n\nTotal Price:\t£'+str(TotalPrice)+'\nNo. of Items:\t'+str(NoofItems)+'\n'
    ReceiptList = ReceiptList+'\nThank you for shopping\nat Jenny\'s Gift Shop.\nWe are happy to accept'
    ReceiptList = ReceiptList+'\nreturns up to 30 days\nfrom purchase in a good\nsaleable condition.\n'
    ReceiptList = ReceiptList+'\nStaff:\t'+str(StaffID)+'\nDate:\t'+str(Date)+'\nTime:\t'+str(Time)
    ReceiptList = ReceiptList+'\n\nTransaction:\t'+str(transactionID)
    receipt.write(ReceiptList) #Write receipt to new file
    receipt.close()
        
    connection.commit()
    connection.close()
    ScannedItems.delete(0, END)
    UpdateTotal(0, 'reset', TotalLabel)
    TransVoidButton.grid_forget()
    SignOffButton.grid(row=4, column=1, padx='10', pady='10')
    if isRefund == False:
        Return_to_Selling()
    elif isRefund == True:
        Return_to_Refund(root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton)
        cancel_refund('B', TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, RefundFuncFrame, RefundFrame, TransIDLabel, NumPadFrame, root, RefundItems, ScannedItems, TotalLabel, FuncFrame, EnterBarcodeLabel, BarcodeEntry)

def GetItems(items, quantity, GiftCards, GiftCardValue, ScannedItems):
    for i in range(0, ScannedItems.size()): #For each item in listbox
        line = ScannedItems.get(i)
        if line[1:3] == 'GC': #If item is a gift card
            GCNumber = line[1:13]
            GiftCards.append(GCNumber) #Append to GCNumber array
            value = line[33:len(line)] #Get gift card value
            GiftCardValue.append(value)
        elif line[1].isdigit() == True: #If item is a product
            StockID = line[1:13] #Get stock ID
            if StockID in items: #If stockID is repeated
                index = items.index(StockID)
                quan = quantity[index] #Increment existing quantity
                del quantity[index]
                quan = quan+1
                quantity.insert(index, quan)
            else:
                items.append(StockID) #Append new item to arrays
                quantity.append(1)

def next_transaction_id():
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Check for existing data
    cursor.execute('SELECT * FROM transactions WHERE transaction_id=100000000000001')
    exist = cursor.fetchone()
    if exist == None: #If table is empty
        nextid = 100000000000001
    else: #If table is not empty, find maximum transaction ID value
        cursor.execute('SELECT MAX(transaction_id) FROM transactions')
        lastid = int(cursor.fetchone()[0])
        nextid = lastid+1 #Get next available transaction ID
    connection.commit()
    connection.close()
    return nextid #Return next available transaction ID
