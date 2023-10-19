import tkinter as tk
import requests
from bs4 import BeautifulSoup

def getSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, "html.parser")

def getBookingText(soup):
    table = soup.find('table', {'class' : 'restable'})
    rows = table.find_all('tr')
    rows = rows[2:]
    text = [ row.get_text() for row in rows ]
    text = [ x.split() for x in text ]
    return text

def formatTime(time):
    return int(time[:2] + time[3:])

def formatRoom(room):
    return int(room[:-1])

def formatBooking(booking):
    start = formatTime(booking[0])
    end = formatTime(booking[2])
    if 'Grupprum,' in booking:
        room = formatRoom(booking[booking.index('Grupprum,') - 1])
    else:
        room = formatRoom(booking[booking.index('Bokningsbar') - 1])
    return [start, end, room]

def getBookedRooms(date, time, text): # returnar bokade grupprum för datumet och tiden
    rooms = []
    add = False
    for line in text:
        if add:
            if 'Ångström' not in line:
                return rooms
            booking = formatBooking(line)
            if booking[0] <= time <= booking[1]:
                rooms.append(booking[2])
        if not add and date in line:
            add = True


def getAvailableRooms(allRooms, bookedRooms):
    return [room for room in allRooms if room not in bookedRooms]

 
url = r'https://cloud.timeedit.net/uu/web/schema/ri1Xc0gw8560YbQQY7ZgZZZX89ZZZX8Y0Cy300pZZZX8a5Y63Q562f5Y7ZZZZX881B6Cvy5G7Yv7yYYd5Yad7Y655agQ7.html'
soup = getSoup(url)
text = getBookingText(soup)

bookings = getBookedRooms('2023-10-22', 2200, text)

list = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 8041, 9040, 9040, 90409]
availableRooms = getAvailableRooms(list, bookings)

print(availableRooms)

def onButtonClick():
    print(userDateEntry.get())

root = tk.Tk()
root.geometry('500x250')
frame = tk.Frame(root)

userDateEntry = tk.Entry(root)
userDateEntry.grid(row=1,column=1)

text = tk.Label(root, text = "Vilket datum? ")
text.grid(row=0, column=0)
dateButton = tk.Button(root, text='Search', command=onButtonClick)
dateButton.grid(row=1, column=0)


frame.place(relx=.5, rely=0.5,anchor= 'center')
text = tk.Label(frame, text="Lediga rum just nu:")
text.grid(row=0, column=0)
for room in availableRooms:
    textLabel = tk.Label(frame, text=str(room))

    textLabel.grid(row=availableRooms.index(room)+1, column=0)

root.protocol('VM_DELETE_WINDOW', lambda : None)
root.mainloop()