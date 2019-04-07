import sqlite3

def tabify(item, width):
    tabsize = width-len(item) #Size of tab
    #Remaining length of string value
    ln = int(((len(item)/tabsize)+1)*tabsize)
    return item.ljust(ln) #Fill with spaces

def UpdateTotal(ItemValue, k, TotalLabel):
    if k == True: #Add to total
        global NoofItems
        global TotalPrice
        NoofItems=int(NoofItems)+1 #Increment NoofItems
        TotalPrice = float(TotalPrice)+float(ItemValue)

    else:
        if k == 'void': #Decrement NoofItems & subtact from total
            NoofItems = int(NoofItems)-1
            TotalPrice = float(TotalPrice) - float(ItemValue)

        elif k == 'Get Total Price':
            return TotalPrice

        elif k == 'Get NoofItems':
            return NoofItems

        elif k == 'reset': #Reset all
            TotalPrice = 0
            NoofItems = 0

        elif k == 'discount':
            TotalPrice = float(TotalPrice) - float(ItemValue)

    TotalPrice = '{:.2f}'.format(TotalPrice) #Update total price label on GUI
    try:
        TotalLabel['text']=tabify('No. of items: '+str(NoofItems), 22)+'Total price: £'+str(TotalPrice)
    except TypeError:
        pass


def clear_entry(root):
    focus = root.focus_get()
    focus.delete(0, 'end')

def set_text(text, root):
    focus = root.focus_get()
    s = focus.get()
    m = s+text
    focus.delete(0, 'end')
    focus.insert(0,m)

def limitSize(entry, size):
    value = entry.get() #Get string
    if len(value) > size:
        entry.set(value[:size]) #Set string
