import datetime
import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from GeneralFunctions_ import *

def Refund(root, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, FuncFrame, BarcodeEntry, EnterBarcodeLabel):
    TransIDEntry.focus()
    root.title('Jenny\'s Gift Shop - Refund')
    EnterBarcodeLabel.grid_forget()
    BarcodeEntry.grid_forget()
    FuncFrame.pack_forget()
    CancelRefundButtonA.grid(row=3, column=3, padx='5', pady='2')
    EnterTransIDLabel.grid(row=0, column=0)
    TransIDEntry.grid(row=1, column=0, padx='15', pady='5')

def confirm_transID_refund(TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, FuncFrame, EnterBarcodeLabel, TotalLabel, ScannedItems, BarcodeEntry, root, NumPadFrame, RefundFuncFrame, TransIDLabel, RefundFrame, RefundItems, RefundTotalLabel):
    CancelRefundButtonA.grid_forget()
    TransactionID = TransIDEntry.get()
    TransIDEntry.delete(0, 'end')
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM transactions WHERE transaction_id=?', [TransactionID])
    row=cursor.fetchone()
    NoofItems=row[5]
    TotalPrice=row[4]
    connection.commit()
    connection.close()
    if row == None:
        TransIDError = Toplevel(bg='#EDFBFF')
        w = 400
        h = 300
        ws = TransIDError.winfo_screenwidth()
        hs = TransIDError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        TransIDError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        TransIDError.title('Transaction ID Error')
        Message(TransIDError, text='ERROR: Transaction ID was not found.', justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
        Button(TransIDError, text='Try Again', justify='center', font=(None,18), width='10', height='4', command=TransIDError.destroy).pack()

    else:
        date = row[2]
        date = date[0:4]+date[5:7]+date[8:10]
        try:
            Thirty = datetime.today() - datetime.timedelta(days=30)
        except AttributeError:
            Thirty = datetime.datetime.today() - datetime.timedelta(days=30)
        Thirty = str(Thirty)
        Thirty = Thirty[0:4]+Thirty[5:7]+Thirty[8:10]
        if int(date) < int(Thirty):
            RefundError = Toplevel(bg='#EDFBFF')
            w = 400
            h = 300
            ws = RefundError.winfo_screenwidth()
            hs = RefundError.winfo_screenheight()
            x = (ws/2)-(w/2)
            y = (hs/2)-(h/2)
            RefundError.geometry('%dx%d+%d+%d' % (w, h, x, y))
            RefundError.title('Refund Error - Date Expired')
            Message(RefundError, text='ERROR: The refund date for this transaction has exceeded 30 days.', justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
            Button(RefundError, text='OK', justify='center', font=(None,18), width='10', height='4', command=RefundError.destroy).pack()
        else:
            root.title('Jenny\'s Gift Shop - Refund')
            TransIDEntry.grid_forget()
            EnterTransIDLabel.grid_forget()
            NumPadFrame.pack_forget()
            FuncFrame.pack_forget()
            RefundFuncFrame.pack(padx='50', pady='100')
            TransIDLabel['text']='Transaction ID:\n'+str(TransactionID)
            TransIDLabel.grid(row=0, column=0)
            RefundFrame.pack(side=RIGHT, padx='10')
            connection = sqlite3.connect('shop.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM transaction_stock WHERE transaction_id=?', [TransactionID])
            TransItems=cursor.fetchall()
            for item in TransItems:
                StockID = str(item[1])
                if StockID[0:2] == 'GC':
                    GCNum = StockID[2:12]
                    GCNum = int(GCNum)
                    cursor.execute('SELECT * FROM gift_cards WHERE gift_card_number=?', [GCNum])
                    row=cursor.fetchone()
                    price = '{:.2f}'.format(row[1])
                    ItemName = 'Gift Card'
                    quantity = 1
                else:
                    quantity = int(item[2])
                    cursor.execute('SELECT * FROM stock WHERE stock_id=?', [StockID])
                    row=cursor.fetchone()
                    price = '{:.2f}'.format(row[2])
                    StockID = row[0]
                    ItemName = row[1]
                for x in range(0, quantity):
                    RefundItems.insert(END, ' '+tabify(str(StockID), 14)+tabify(str(ItemName), 17)+'£'+str(price))
                    ScannedItems.insert(END, '  ')
            RefundTotalLabel['text']=tabify('No. of items: '+str(NoofItems), 22)+'Total price: £'+str(TotalPrice)
            connection.commit()
            connection.close()

def cancel_refund(k, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, RefundFuncFrame, RefundFrame, TransIDLabel, NumPadFrame, root, RefundItems, ScannedItems, TotalLabel, FuncFrame, EnterBarcodeLabel, BarcodeEntry):
    if k == 'A':
        TransIDEntry.grid_forget()
        EnterTransIDLabel.grid_forget()
        CancelRefundButtonA.grid_forget()
    elif k == 'B':
        RefundFuncFrame.pack_forget()
        RefundFrame.pack_forget()
        TransIDLabel.grid_forget()
        NumPadFrame.pack(side=BOTTOM, pady='20')
    root.title('Jenny\'s Gift Shop - Cashier')
    RefundItems.delete(0, 'end')
    ScannedItems.delete(0, 'end')
    TransIDEntry.delete(0, 'end')
    UpdateTotal(0, 'reset', TotalLabel)
    FuncFrame.pack(side=RIGHT, padx='10', pady='10')
    EnterBarcodeLabel.grid(row=0, column=0)
    BarcodeEntry.grid(row=1, column=0, padx='15', pady='5')
    BarcodeEntry.focus()

def add_to_refund(RefundItems, ScannedItems, TotalLabel):
    focus = RefundItems.curselection()[0]
    line = RefundItems.get(focus)
    if line[1:3] == 'GC':
        RefundError = Toplevel(bg='#EDFBFF')
        w = 400
        h = 300
        ws = RefundError.winfo_screenwidth()
        hs = RefundError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        RefundError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        RefundError.title('Refund Error - Cannot Refund Gift Cards')
        Message(RefundError, text='ERROR: Gift Cards cannot be refunded.', justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
        Button(RefundError, text='OK', justify='center', font=(None,18), width='10', height='4', command=RefundError.destroy).pack()
    else:
        ExistLine = ScannedItems.get(focus)
        if line == ExistLine:
            RefundError = Toplevel(bg='#EDFBFF')
            w = 400
            h = 300
            ws = RefundError.winfo_screenwidth()
            hs = RefundError.winfo_screenheight()
            x = (ws/2)-(w/2)
            y = (hs/2)-(h/2)
            RefundError.geometry('%dx%d+%d+%d' % (w, h, x, y))
            RefundError.title('Refund Error - Item Already Added')
            Message(RefundError, text='ERROR: This item has already been added to the refund.', justify='center', font=(None, 18), bg='#EDFBFF', width='250').pack()
            Button(RefundError, text='OK', justify='center', font=(None,18), width='10', height='4', command=RefundError.destroy).pack()
        else:
            price = line[33:len(line)]
            price = 0-float(price) #Negative price
            ScannedItems.delete(focus) #Insert item into equal
            ScannedItems.insert(focus, line) #index position
            UpdateTotal(price, True, TotalLabel)
            RefundItems.selection_clear(focus)

def complete_refund(root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton, TotalPricePayLabel, CashPaidLabel, ChangeDueLabel):
    root.title('Jenny\'s Gift Shop - Refund Payment')
    RefundFrame.pack_forget()
    RefundFuncFrame.pack_forget()
    NumPadFrame.pack(side=BOTTOM, pady='20')
    PayFuncFrame.pack(side=RIGHT, padx='30', pady='10')
    PayFuncFrameBottom.pack_forget()
    ReturnRefundButton.grid(row=3, column=3, padx='5', pady='2')
    EnterButton.grid_forget()
    ConfirmRefundButton.grid(row=1, column=3, rowspan=2, padx='5', pady='2')
    TotalPrice = UpdateTotal(0, 'Get Total Price', 0)
    TotalPrice = float(TotalPrice)
    TotalPrice = '{:.2f}'.format(TotalPrice)
    TotalPricePayLabel['text']='Total: £'+str(TotalPrice)
    CashPaidLabel['text']='Cash Paid: £0.00'
    ChangeDue = abs(float(TotalPrice))
    ChangeDueLabel['text']='Change Due: £'+str(ChangeDue)

def Return_to_Refund(root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton):
    root.title('Jenny\'s Gift Shop - Refund')
    RefundFrame.pack(side=RIGHT, padx='10')
    RefundFuncFrame.pack(padx='50', pady='100')
    NumPadFrame.pack_forget()
    PayFuncFrame.pack_forget()
    PayFuncFrameBottom.pack(side=BOTTOM)
    ReturnRefundButton.grid_forget()
    EnterButton.grid(row=1, column=3, rowspan=2, padx='5', pady='2')
    ConfirmRefundButton.grid_forget()
