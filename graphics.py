import tkinter as tk
import requests
from bs4 import BeautifulSoup
import ÅngstRooms

 
# Funktionen returnernar en funktion eftersom den returnerade funktionen måste sparas i en variabel på line 91
# För att kunna användas i button command= param
def onButtonClick(root, userDateEntry, userTimeEntry):
    def returnFunction():
        global availableRooms
        date = userDateEntry.get()
        time = userTimeEntry.get()
        
        if date == '' and time == '':
            return
        allRooms = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 80412, 90402, 90403, 90409]
        url = r'https://cloud.timeedit.net/uu/web/schema/ri1Xc0gw8560YbQQY7ZgZZZX89ZZZX8Y0Cy300pZZZX8a5Y63Q562f5Y7ZZZZX881B6Cvy5G7Yv7yYYd5Yad7Y655agQ7.html'
        availableRooms = ÅngstRooms.available(url,allRooms, date, int(time))
        print(time)
        root.quit()
    return returnFunction


def firstWindow():
    root = tk.Tk()
    root.geometry('500x250')

    userDateEntry = tk.Entry(root)
    userDateEntry.grid(row=1,column=1)

    userTimeEntry = tk.Entry(root)
    userTimeEntry.grid(row=1,column=2)

    dateText = tk.Label(root, text = "Datum (ÅÅÅÅ-MM-DD)")
    dateText.grid(row=0, column=1)

    timeText = tk.Label(root, text = "Tid (XXXX)")
    timeText.grid(row=0, column=2)

    onButtonClickWithArgs = onButtonClick(root, userDateEntry, userTimeEntry)
    dateButton = tk.Button(root, text='Search', command=onButtonClickWithArgs)
    dateButton.grid(row=1, column=0)

    root.protocol('VM_DELETE_WINDOW', lambda : None)
    root.mainloop()
  
def secondWindow():
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.place(relx=.5, rely=0.5,anchor= 'center')
    text = tk.Label(frame, text="Lediga rum :")
    text.grid(row=0, column=0)
    for room in availableRooms:
    
        textLabel = tk.Label(frame, text=str(str(room[0]) + " " + str(room[1])))
        textLabel.grid(row=availableRooms.index(room)+1, column=0)
    root.mainloop()
firstWindow()
secondWindow()
