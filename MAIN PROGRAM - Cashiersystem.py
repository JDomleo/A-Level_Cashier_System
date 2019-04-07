#Import relevant libraries needed
import datetime
import winsound
import sqlite3
from tkinter import *
from tkinter import Tk, StringVar, ttk
from ViewStaff_ import *
from ViewStock_ import *
from GeneralFunctions_ import *
from PriceCheck_ import *
from DiscountVoid_ import *
from GiftCards_ import *
from Payment_ import *
from Refund_ import *

def clock(*args): #Automatically updates date and time
    date = datetime.datetime.today().strftime('Date: %d %b %Y')
    TodayDate['text'] = date #Updates date label
    time = datetime.datetime.now().strftime('Time: %H:%M:%S')
    CurrentTime['text'] = time #Updates time label
    root.after(1000, clock) #Run itself again after 1sec

def LoginScreen(*args): #Start up screen
    root.title('Jenny\'s Gift Shop - Login')
    ImageFrame.pack(side=LEFT, padx='20', pady='10')
    LoginFrame.pack(side=RIGHT, padx='30')
    CentreFrame.pack(side=LEFT, padx='15', pady='10')

def Login(*args):
    user_login=StaffNumberEntry.get() #When 'login' button is clicked, checked if details are correct
    user_password=PasswordEntry.get() #Get values from entry boxes
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor() #Find record in employee table where staff ID AND password match
    cursor.execute('SELECT * FROM employee WHERE staff_ID=? AND password=?', [user_login, user_password])
    row = cursor.fetchone()
    if row != None: #If record does exist
        position = row[4]
        StaffNumberLabel['text'] = 'Staff ID: '+str(row[0]) #Update Information Frame
        StaffNameLabel['text'] = 'Name: '+str(row[2])+' '+str(row[3])
        PositionLabel['text'] = 'Position: '+str(position)
        position = position.lower()
        if 'manager' not in position: #Check if position is managerial
            if 'programmer' not in position: # Check if programmer
                ViewStaffButton['state'] = 'disabled'
        LoginFrame.pack_forget()
        ImageFrame.pack_forget() #Hide frames from login screen
        CentreFrame.pack_forget()
        connection.commit()
        connection.close()      #Run function to display frames relevant for the main screen
        MainScreen()
        

    elif row == None: #If record does NOT exist
        LoginError = Toplevel(bg='#EDFBFF') #Display top-level window as error
        w = 200
        h = 180
        ws = LoginError.winfo_screenwidth()
        hs = LoginError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        LoginError.geometry('%dx%d+%d+%d' % (w, h, x, y)) #Display error in centre of screen
        LoginError.title('Login Failure')
        LoginErrorMsg = Message(LoginError, text='ERROR:\nIncorrect Staff ID\nor Password',
                                justify='center', font='bold', bg='#EDFBFF').pack()
        LoginErrorButton = Button(LoginError, text='Try Again', font=(None, 20), width='8',
                                  height='2', command=LoginError.destroy).pack(padx='10', pady='5')
        StaffNumberEntry.delete(0,END) #Clear the Staff ID and Password entry boxes,
        PasswordEntry.delete(0,END)    #and set focus in Staff ID entry box, so the
        StaffNumberEntry.focus()       #user can try again.
        connection.commit()
        connection.close()

def append_barcode(*args):
    barcode = BarcodeEntry.get() #Get barcode entered by user
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM stock WHERE stock_id=?', [barcode]) #Search barcode in database
    row = cursor.fetchone()
    if row != None: #If barcode is found
        price = '{:.2f}'.format(row[2])     #Add item to end of ScannedItems list box
        ScannedItems.insert(END, ' '+tabify(str(row[0]), 14)+tabify(str(row[1]), 17)+'£'+str(price))
        UpdateTotal(price, True, TotalLabel) #Update total price and no. of items label
        SignOffButton.grid_forget() #If an item has been added, the user is not able to sign off,
                                    #therefore the sign off button is hidden.
        
        TransVoidButton.grid(row=4, column=1, padx='10', pady='10') #The 'Transaction Void' button
            #replaces the sign off button, allowing the user to void ALL items from the ScannedItems
            #list and start the transaction over from scratch.
        
        SubtotalButton.grid(row=3, column=3, padx='5', pady='2') #As soon as an item is added to the
            #list, the 'Subtotal' button will appear, so the user can finish the transaction

        #Beep when item is scanned
        frequency = 750
        duration = 350
        winsound.Beep(frequency, duration)

    elif row == None: #If barcode is NOT found
        BarcodeError = Toplevel(bg='#EDFBFF')
        w = 200
        h = 250
        ws = BarcodeError.winfo_screenwidth()
        hs = BarcodeError.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        BarcodeError.geometry('%dx%d+%d+%d' % (w, h, x, y))
        BarcodeError.title('Barcode Failure')
        if len(barcode) < 12: #Length check: must be exactly 12 digits
            Message(BarcodeError, bg='#EDFBFF', text='ERROR:\nBarcodes must\nbe 12 digits.',
                    justify='center', font='bold').pack()
        else: ##Barcode has not been added yet
            Message(BarcodeError, bg='#EDFBFF', text='ERROR:\nBarcode does not exist yet.',
                    justify='center', font='bold').pack()
        Button(BarcodeError, text='Try Again', font=(None, 20), width='8', height='2',
               command=BarcodeError.destroy).pack(padx='10', pady='10')
    BarcodeEntry.delete(0,END)
    connection.commit()
    connection.close()

def enter(*args):
    focus = root.focus_get()
    if focus == StaffNumberEntry:
        PasswordEntry.focus()
    elif focus == PasswordEntry:
        Login()
    elif focus == BarcodeEntry:
        append_barcode()
    elif focus == TransIDEntry: 
        confirm_transID_refund(TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, FuncFrame, EnterBarcodeLabel, TotalLabel, ScannedItems, BarcodeEntry, root, NumPadFrame, RefundFuncFrame, TransIDLabel, RefundFrame, RefundItems, RefundTotalLabel)

def MainScreen(*args): #Display widgets relevant for main screen
    root.title('Jenny\'s Gift Shop - Cashier')
    ScannedItemsFrame.pack(side=LEFT, padx='10', pady='10')
    CentreFrame.pack(side=LEFT, padx='20', pady='10')
    EnterBarcodeCashFrame.pack(side=TOP, pady='20') 
    FuncFrame.pack(side=RIGHT, padx='10', pady='10')
    PointButton.grid(row=3, column=2, padx='2', pady='2')
    BarcodeEntry.focus() #Focus the barcode entry box automatically

def SignOff(*args):
    root.title('Jenny\'s Gift Shop - Login')
    ScannedItemsFrame.pack_forget()
    EnterBarcodeCashFrame.pack_forget()
    FuncFrame.pack_forget() #Revert all widgets back to their
    CentreFrame.pack_forget() #origional state
    SubtotalButton.grid_forget()
    PointButton.grid_forget()
    StaffNumberLabel['text'] = 'Staff ID: '
    StaffNameLabel['text'] = 'Staff Name: '
    PositionLabel['text'] = 'Position: '
    ViewStaffButton['state'] = 'normal'
    StaffNumberEntry.delete(0,END) #Clear the Staff ID and
    StaffNumberEntry.focus() #Password entry boxes and set the
    PasswordEntry.delete(0,END) #Staff ID entry as the focus
    #Run the LoginScreen function as if the program were just
    #starting up
    LoginScreen()

def Subtotal(*args):
    root.title('Jenny\'s Gift Shop - Payment')
    SubtotalButton.grid_forget()
    ReturnSellButton.grid(row=3, column=3, padx='5', pady='2')
    EnterButton.grid_forget()
    CompleteTransactionButton.grid(row=1, column=3, rowspan=2, padx='5', pady='2')
    EnterBarcodeLabel.grid_forget()
    BarcodeEntry.grid_forget()
    FuncFrame.pack_forget()
    PayFuncFrame.pack(side=RIGHT, padx='10', pady='10')
    EnterCashLabel.grid(row=0, column=0) #Display 'Enter Cash' label and entry box
    CashEntry.grid(row=1, column=0, padx='15', pady='5')
    CashEntry.focus()
    TotalPrice = UpdateTotal(0, 'Get Total Price', 0)
    TotalPrice = float(TotalPrice)
    TotalPrice = '{:.2f}'.format(TotalPrice)
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    connection.commit()
    connection.close()
    TotalPricePayLabel['text']='Total: £'+str(TotalPrice)
    TotalPrice = float(TotalPrice)
    EasyAccess=[1, 5, 10, 20] #Arrays
    TextPound=[OnePoundButton, FivePoundButton, TenPoundButton, TwentyPoundButton]
    for i in range(0, len(EasyAccess)):
        if EasyAccess[i] < TotalPrice: #Less than total price
            DisableButton = TextPound[i]
            DisableButton['state']='disabled'
        elif EasyAccess[i] >= TotalPrice: #Greater than total price
            break

def Return_to_Selling(*args):
    root.title('Jenny\'s Gift Shop - Cashier')
    ReturnSellButton.grid_forget()
    SubtotalButton.grid(row=3, column=3, padx='5', pady='2')
    CompleteTransactionButton.grid_forget()
    EnterButton.grid(row=1, column=3, rowspan=2, padx='5', pady='2')
    PayFuncFrame.pack_forget()
    FuncFrame.pack(side=RIGHT, padx='10', pady='10')
    EnterCashLabel.grid_forget()
    EnterBarcodeLabel.grid(row=0, column=0)
    CashEntry.grid_forget()
    CashEntry.delete(0, END)
    BarcodeEntry.grid(row=1, column=0, padx='15', pady='5')
    BarcodeEntry.delete(0, END)
    BarcodeEntry.focus()
    CashPaidLabel['text'] = 'Cash Paid:'
    ChangeDueLabel['text'] = 'Change Due:'
    OnePoundButton['state']='normal'
    FivePoundButton['state']='normal'
    TenPoundButton['state']='normal'
    TwentyPoundButton['state']='normal'

#ScannedItems, TransVoidButton, SignOffButton, TotalLabel
def TransVoid(*args):
    Items = ScannedItems.size()
    for item in range(0, Items):
        ScannedItems.delete(item)
    ScannedItems.delete(0)
    UpdateTotal(0, 'reset', TotalLabel)
    TransVoidButton.grid_forget()
    SignOffButton.grid(row=4, column=1, padx='10', pady='10')
    SubtotalButton.grid_forget()
    

        #Create SQL database
connection = sqlite3.connect('shop.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
staff_ID INTEGER PRIMARY KEY,
password INTEGER,
fname TEXT,
lname TEXT,
position TEXT);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
stock_id INTEGER PRIMARY KEY,
item_name TEXT,
unit_price REAL,
no_in_stock INTEGER);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
transaction_id INTEGER PRIMARY KEY,
staff_ID INTEGER,
date TEXT,
time TEXT,
Total_Price REAL,
No_of_Items INTEGER,
Cash_Paid REAL,
Change_Due REAL,
Gift_Card_Used INTEGER,
is_Refund INTEGER);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transaction_stock (
transaction_id INTEGER,
stock_id INTEGER,
quantity INTEGER,
quan_price REAL,
refunded INTEGER);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS gift_card_transaction (
gift_card_number INTEGER,
transaction_id INTEGER,
Gift_Card_Value_Paid REAL);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS gift_cards (
gift_card_number INTEGER PRIMARY KEY,
initial_value REAL,
date_purchased TEXT,
current_value REAL);''')


cursor.execute('SELECT * FROM employee WHERE staff_ID=1001')
exist = cursor.fetchone()
if exist == None:
    cursor.execute('''INSERT INTO employee (staff_ID, password, fname, lname, position)
        VALUES ('1001', '1234', 'Test', 'Example', 'Manager');''')
connection.commit()
connection.close()


'''Root Window'''
root = Tk()
root.title('Jenny\'s Gift Shop')
root.state('zoomed')    #Full Screen
root.configure(background='#EDFBFF') #Light Blue


'''ALL SCREENS - Information Frame'''
InfoFrame = Frame(root) #Create a frame called InfoFrame in the root window
InfoFrame.configure(background='#EDFBFF')   #Display relevant information labels
StaffNumberLabel = Label(InfoFrame, width='35', relief='groove', font=(None, 11), text='Staff ID: ')
StaffNumberLabel.pack(padx=20, pady=5, side=LEFT, ipady=2, ipadx=2)
StaffNameLabel = Label(InfoFrame, width='35', relief='groove', font=(None, 11), text='Staff Name: ')
StaffNameLabel.pack(padx=20, pady=5, side=LEFT, ipady=2, ipadx=2)
PositionLabel = Label(InfoFrame, width='35', relief='groove', font=(None, 11), text='Position: ')
PositionLabel.pack(padx=20, pady=5, side=LEFT, ipady=2, ipadx=2)
TodayDate = Label(InfoFrame, width='20', relief='groove', font=(None, 11))
TodayDate.pack(padx=20, pady=5, side=LEFT, ipady=2, ipadx=2)
CurrentTime = Label(InfoFrame, width='20', relief='groove', font=(None, 11))
CurrentTime.pack(padx=20, pady=5, side=LEFT, ipady=2, ipadx=2)
InfoFrame.pack() #Display InfoFrame at top of window (permanent)



'''Shop Logo - Image Frame'''
ImageFrame = Frame(root) #Create a frame called ImageFrame in the root window
LogoImage = PhotoImage(file="shop_logo.gif")
LogoPhoto = LogoImage.subsample(2, 2) #Scale the photo in proportion
Label(ImageFrame, image=LogoPhoto, width='480', height='500', bg='#FFFFFF').pack()



'''LOGIN SCREEN - Login Frame'''
LoginFrame = Frame(root) #Create a frame called LoginFrame in the root window
LoginFrame.configure(background='#EDFBFF')
            #Display staff_ID and password entry boxes and 'login' button
StaffIDVar = StringVar()
StaffIDVar.trace('w', lambda *args: limitSize(StaffIDVar, 4))
StaffNumberEntry = Entry(LoginFrame,  justify='center', font=(None, 40), width='10', textvariable=StaffIDVar)
StaffNumberEntry.pack(pady='10')
StaffNumberEntry.focus()
PasswordVar = StringVar()
PasswordVar.trace('w', lambda *args: limitSize(PasswordVar, 4))
PasswordEntry = Entry(LoginFrame, show='*', justify='center', font=(None, 40), width='6', textvariable=PasswordVar)
PasswordEntry.pack(pady='10')



'''MAIN & PAYMENT SCREENS - ScannedItemsFrame'''
ScannedItemsFrame=Frame(root) #Create a frame called ScannedItemsFrame in the root window
ScannedItemsFrame.configure(width='480', height='640')
ScannedItemsFrame.pack_propagate(0)

Label(ScannedItemsFrame, font = 'Courier', bg='#FFFFFF', width='450', text='  '+tabify('Stock ID', 14)+tabify('Item Name', 17)+'Price', anchor='w').pack(side=TOP)

ListboxFrame = Frame(ScannedItemsFrame)
ListboxFrame.configure(width='480')
ScannedItems = Listbox(ListboxFrame, font = 'Courier')
ScannedItems.config(width='45', height='31')
ScannedItems.pack(side=LEFT)
ScannedItemsScrollbar = Scrollbar(ListboxFrame)
ScannedItemsScrollbar.pack(side=RIGHT, fill=Y)
ScannedItems.config(yscrollcommand=ScannedItemsScrollbar.set)
ScannedItemsScrollbar.config(command=ScannedItems.yview)
ListboxFrame.pack(side=TOP)

TotalLabel = Label(ScannedItemsFrame, font = 'Courier', bg='#FFFFFF', width='450')
TotalLabel.pack(side=BOTTOM, anchor='w')
UpdateTotal(0, 'reset', TotalLabel)



'''ALL SCREENS - CENTRE FRAME'''
CentreFrame=Frame(root) #Create a frame called CentreFrame in the root window,
CentreFrame.configure(background='#EDFBFF') #this will display the number pad and enter barcode

        #MAIN SCREEN - Enter Barcode Entry Box
EnterBarcodeCashFrame=Frame(CentreFrame) #Create a frame called EnterBarcodeFrame in the CentreFrame
EnterBarcodeCashFrame.configure(background='#EDFBFF')
BarcodeVar = StringVar()
BarcodeVar.trace('w', lambda *args: limitSize(BarcodeVar, 12))
EnterBarcodeLabel = Label(EnterBarcodeCashFrame, text='Enter Barcode', font=(None, 25), background='#EDFBFF')
EnterBarcodeLabel.grid(row=0, column=0) #Display 'Enter Barcode' label and entry box
BarcodeEntry = Entry(EnterBarcodeCashFrame, width='14', justify='center', font=(None, 30), textvariable=BarcodeVar)
BarcodeEntry.grid(row=1, column=0, padx='15', pady='5')

RefundVar = StringVar()
RefundVar.trace('w', lambda *args: limitSize(RefundVar, 15))
EnterTransIDLabel = Label(EnterBarcodeCashFrame, text='Enter Transaction ID', font=(None, 25), background='#EDFBFF')
TransIDEntry = Entry(EnterBarcodeCashFrame, width='16', justify='center', font=(None, 30), textvariable=RefundVar)

        #ALL SCREENS - Number Pad Buttons
NumPadFrame = Frame(CentreFrame) #Create a frame called NumPadFrame in the CentreFrame
NumPadFrame.configure(background='#EDFBFF') #Display buttons from 0-9, 00, clear, enter and subtotal
SevenButton = Button(NumPadFrame, text='7', width='10', height='4', font=(None, 18), command=lambda:set_text('7', root))
SevenButton.grid(row=0, column=0, padx='2', pady='2')
EightButton = Button(NumPadFrame, text='8', width='10', height='4', font=(None, 18), command=lambda:set_text('8', root))
EightButton.grid(row=0, column=1, padx='2', pady='2')
NineButton = Button(NumPadFrame, text='9', width='10', height='4', font=(None, 18), command=lambda:set_text('9', root))
NineButton.grid(row=0, column=2, padx='2', pady='2')
ClearButton = Button(NumPadFrame, text='Clear', width='10', height='4', font=(None, 18), command=lambda: clear_entry(root))
ClearButton.grid(row=0, column=3, padx='5', pady='2')
FourButton = Button(NumPadFrame, text='4', width='10', height='4', font=(None, 18), command=lambda:set_text('4', root))
FourButton.grid(row=1, column=0, padx='2', pady='2')
FiveButton = Button(NumPadFrame, text='5', width='10', height='4', font=(None, 18), command=lambda:set_text('5', root))
FiveButton.grid(row=1, column=1, padx='2', pady='2')
SixButton = Button(NumPadFrame, text='6', width='10', height='4', font=(None, 18), command=lambda:set_text('6', root))
SixButton.grid(row=1, column=2, padx='2', pady='2')
EnterButton = Button(NumPadFrame, text='Enter', width='10', height='9', font=(None, 18), command=enter)
EnterButton.grid(row=1, column=3, rowspan=2, padx='5', pady='2')
CompleteTransactionButton = Button(NumPadFrame, text='Complete\nTransaction', width='10', height='9', font=(None, 18), command=lambda: complete_transaction(CashPaidLabel, ChangeDueLabel, StaffNumberLabel, ScannedItems, TransVoidButton, SignOffButton, TotalLabel, Return_to_Selling, Return_to_Refund, cancel_refund, root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, TransIDLabel, EnterBarcodeLabel, BarcodeEntry, RefundItems, FuncFrame))
ConfirmRefundButton= Button(NumPadFrame, text='Confirm\nRefund', width='10', height='9', font=(None, 18), command=lambda: complete_transaction(CashPaidLabel, ChangeDueLabel, StaffNumberLabel, ScannedItems, TransVoidButton, SignOffButton, TotalLabel, Return_to_Selling, Return_to_Refund, cancel_refund, root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, TransIDLabel, EnterBarcodeLabel, BarcodeEntry, RefundItems, FuncFrame))
OneButton = Button(NumPadFrame, text='1', width='10', height='4', font=(None, 18), command=lambda:set_text('1', root))
OneButton.grid(row=2, column=0, padx='2', pady='2')
TwoButton = Button(NumPadFrame, text='2', width='10', height='4', font=(None, 18), command=lambda:set_text('2', root))
TwoButton.grid(row=2, column=1, padx='2', pady='2')
ThreeButton = Button(NumPadFrame, text='3', width='10', height='4', font=(None, 18), command=lambda:set_text('3', root))
ThreeButton.grid(row=2, column=2, padx='2', pady='2')
ZeroZeroButton = Button(NumPadFrame, text='00', width='10', height='4', font=(None, 18), command=lambda:set_text('00', root))
ZeroZeroButton.grid(row=3, column=0, padx='2', pady='2')
ZeroButton = Button(NumPadFrame, text='0', width='10', height='4', font=(None, 18), command=lambda:set_text('0', root))
ZeroButton.grid(row=3, column=1, padx='2', pady='2')
PointButton = Button(NumPadFrame, text='.', width='10', height='4', font=(None, 18), command=lambda:set_text('.', root))
SubtotalButton = Button(NumPadFrame, text='Subtotal', width='10', height='4', font=(None, 18), command=Subtotal)
CancelRefundButtonA = Button(NumPadFrame, text='Cancel\nRefund', width='10', height='4', font=(None, 18), command=lambda: cancel_refund('A', TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, RefundFuncFrame, RefundFrame, TransIDLabel, NumPadFrame, root, RefundItems, ScannedItems, TotalLabel, FuncFrame, EnterBarcodeLabel, BarcodeEntry))
ReturnSellButton = Button(NumPadFrame, text='Return to\nSelling', width='10', height='4', font=(None, 18), command=lambda: Return_to_Selling(root, SubtotalButton, ReturnSellButton, EnterButton, CompleteTransactionButton, EnterBarcodeLabel, BarcodeEntry, FuncFrame, PayFuncFrame, EnterCashLabel, CashEntry, TotalPricePayLabel, OnePoundButton, FivePoundButton, TenPoundButton, TwentyPoundButton))
ReturnRefundButton = Button(NumPadFrame, text='Return to\nRefund', width='10', height='4', font=(None, 18), command=lambda: Return_to_Refund(root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton))
NumPadFrame.pack(side=BOTTOM, pady='20')




'''MAIN SCREEN - Function Button Frame'''
        #Function Buttons layout
FuncFrame = Frame(root) #Create a frame called FuncFrame in the root window
FuncFrame.configure(background='#EDFBFF') #Display relevant function buttons
ViewStaffButton = Button(FuncFrame, text='View\nStaff', width='12', height='4', font=(None, 16), command=view_staff)
ViewStaffButton.grid(row=0, column=1, padx='10', pady='10')
PriceCheckButton = Button(FuncFrame, text='Price\nCheck', width='12', height='4', font=(None, 16), command=lambda: price_check(TotalLabel, ScannedItems, BarcodeEntry))
PriceCheckButton.grid(row=1, column=0, padx='10', pady='10')
ViewStockButton = Button(FuncFrame, text='View\nStock', width='12', height='4', font=(None, 16), command=view_stock)
ViewStockButton.grid(row=1, column=1, padx='10', pady='10')
VoidItemButton = Button(FuncFrame, text='Void\nItem', width='12', height='4', font=(None, 16), command=lambda: Void(TotalLabel, ScannedItems, BarcodeEntry))
VoidItemButton.grid(row=2, column=0, padx='10', pady='10')
DiscountButton = Button(FuncFrame, text='Discount\n%', width='12', height='4', font=(None, 16), command=lambda: Discount(TotalLabel, ScannedItems, BarcodeEntry))
DiscountButton.grid(row=2, column=1, padx='10', pady='10')
GiftCardEnquiryButton = Button(FuncFrame, text='Gift Card\nEnquiry', width='12', height='4', font=(None, 16), command=gift_card_enquiry)
GiftCardEnquiryButton.grid(row=3, column=0, padx='10', pady='10')
GiftCardSaleButton = Button(FuncFrame, text='Gift Card\nSale', width='12', height='4', font=(None, 16), command=lambda: gift_card_sale(TotalLabel, BarcodeEntry, ScannedItems, SignOffButton, TransVoidButton, SubtotalButton))
GiftCardSaleButton.grid(row=3, column=1, padx='10', pady='10')
RefundButton = Button(FuncFrame, text='Refund', width='12', height='4', font=(None, 16), command =lambda: Refund(root, TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, FuncFrame, BarcodeEntry, EnterBarcodeLabel))
RefundButton.grid(row=4, column=0, padx='10', pady='10')
SignOffButton = Button(FuncFrame, text='Sign\nOff', width='12', height='4', font=(None, 16), command=SignOff)
SignOffButton.grid(row=4, column=1, padx='10', pady='10')
TransVoidButton = Button(FuncFrame, text='Trans\nVoid', width='12', height='4', font=(None, 16), command=TransVoid)


'''PAYMENT SCREEN'''
CashVar = StringVar()
CashVar.trace('w', lambda *args: limitSize(CashVar, 7))
EnterCashLabel = Label(EnterBarcodeCashFrame, text='Enter Cash Amount', font=(None, 25), bg='#EDFBFF')
CashEntry = Entry(EnterBarcodeCashFrame, width='14', justify='center', font=(None, 30), textvariable=CashVar)

PayFuncFrame = Frame(root)
PayFuncFrame.configure(background='#EDFBFF')
PayFuncFrameTop = Frame(PayFuncFrame)
PayFuncFrameTop.configure(background='#EDFBFF')
TotalPricePayLabel = Label(PayFuncFrameTop, text='Total:', font=(None, 25), bg='#EDFBFF')
TotalPricePayLabel.pack(padx='10', pady='8')
CashPaidLabel = Label(PayFuncFrameTop, text='Cash Paid:', font=(None, 25), bg='#EDFBFF')
CashPaidLabel.pack(padx='10', pady='8')
ChangeDueLabel = Label(PayFuncFrameTop, text='Change Due:', font=(None, 25), bg='#EDFBFF')
ChangeDueLabel.pack(padx='10', pady='8')
PayFuncFrameTop.pack(side=TOP)
PayFuncFrameBottom = Frame(PayFuncFrame)
PayFuncFrameBottom.configure(background='#EDFBFF')
ExactCashButton = Button(PayFuncFrameBottom, text='Exact\nCash', width='12', height='4', font=(None, 16), command=lambda: payment('Exact Cash', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
ExactCashButton.grid(row=0, column=0, padx='10', pady='10')
OnePoundButton = Button(PayFuncFrameBottom, text='£1', width='12', height='4', font=(None, 16), command=lambda: payment('1', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
OnePoundButton.grid(row=0, column=1, padx='10', pady='10')
CashButton = Button(PayFuncFrameBottom, text='Cash', width='12', height='4', font=(None, 16), command=lambda: payment('Cash', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
CashButton.grid(row=1, column=0, padx='10', pady='10')
FivePoundButton = Button(PayFuncFrameBottom, text='£5', width='12', height='4', font=(None, 16), command=lambda: payment('5', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
FivePoundButton.grid(row=1, column=1, padx='10', pady='10')
GiftCardButton = Button(PayFuncFrameBottom, text='Gift\nCard', width='12', height='4', font=(None, 16), command = lambda: GCPayment(TotalPricePayLabel, CashPaidLabel, ChangeDueLabel))
GiftCardButton.grid(row=2, column=0, padx='10', pady='10')
TenPoundButton = Button(PayFuncFrameBottom, text='£10', width='12', height='4', font=(None, 16), command=lambda: payment('10', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
TenPoundButton.grid(row=2, column=1, padx='10', pady='10')
CardsButton = Button(PayFuncFrameBottom, text='Cards', width='12', height='4', state='disabled', font=(None, 16))
CardsButton.grid(row=3, column=0, padx='10', pady='10')
TwentyPoundButton = Button(PayFuncFrameBottom, text='£20', width='12', height='4', font=(None, 16), command=lambda: payment('20', TotalPricePayLabel, ChangeDueLabel, CashPaidLabel, CashEntry))
TwentyPoundButton.grid(row=3, column=1, padx='10', pady='10')
PayFuncFrameBottom.pack(side=BOTTOM)

'''Refund Screen'''
RefundFuncFrame = Frame(CentreFrame)
RefundFuncFrame.configure(background='#EDFBFF')
RemoveRefundButton = Button(RefundFuncFrame, text='Remove from\nRefund', width='12', height='4', font=(None, 18))
RemoveRefundButton.grid(column=0, row=0, padx='10', pady='8')
AddtoRefundButton = Button(RefundFuncFrame, text='Add to\nRefund', width='12', height='4', font=(None, 18), command=lambda: add_to_refund(RefundItems, ScannedItems, TotalLabel))
AddtoRefundButton.grid(column=1, row=0, padx='10', pady='8')
CancelRefundButtonB = Button(RefundFuncFrame, text='Cancel\nRefund', width='12', height='4', font=(None, 18), command=lambda: cancel_refund('B', TransIDEntry, EnterTransIDLabel, CancelRefundButtonA, RefundFuncFrame, RefundFrame, TransIDLabel, NumPadFrame, root, RefundItems, ScannedItems, TotalLabel, FuncFrame, EnterBarcodeLabel, BarcodeEntry))
CancelRefundButtonB.grid(column=0, row=1, padx='10', pady='8')
CompleteRefundButton = Button(RefundFuncFrame, text='Complete\nRefund', width='12', height='4', font=(None, 18), command=lambda: complete_refund(root, RefundFrame, RefundFuncFrame, NumPadFrame, PayFuncFrame, PayFuncFrameBottom, ReturnRefundButton, EnterButton, ConfirmRefundButton, TotalPricePayLabel, CashPaidLabel, ChangeDueLabel))
CompleteRefundButton.grid(column=1, row=1, padx='10', pady='8')

RefundFrame = Frame(root)
RefundFrame.configure(width='480', height='640')
RefundFrame.pack_propagate(0)
Label(RefundFrame, font = 'Courier', bg='#FFFFFF', width='450', text='  '+tabify('Stock ID', 14)+tabify('Item Name', 17)+'Price', anchor='w').pack(side=TOP)

RefundListboxFrame = Frame(RefundFrame)
RefundListboxFrame.configure(width='480')
RefundItems = Listbox(RefundListboxFrame, font = 'Courier')
RefundItems.config(width='45', height='31')
RefundItems.pack(side=LEFT)
RefundItemsScrollbar = Scrollbar(RefundListboxFrame)
RefundItemsScrollbar.pack(side=RIGHT, fill=Y)
RefundItems.config(yscrollcommand=RefundItemsScrollbar.set)
RefundItemsScrollbar.config(command=RefundItems.yview)
RefundListboxFrame.pack(side=TOP)

RefundTotalLabel = Label(RefundFrame, font = 'Courier', bg='#FFFFFF', width='450')
RefundTotalLabel.pack(side=BOTTOM, anchor='w')

TransIDLabel = Label(EnterBarcodeCashFrame, font=(None, 25), background='#EDFBFF')


clock() #FIRST, run the clock function which repeats itself every 1000ms

LoginScreen() #THEN, run the LoginScreen function to display the widgets upon startup of program


root.mainloop()
