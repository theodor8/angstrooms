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

def getAllBookings(date, text): # returnar alla bokningar för ett visst datum
    rooms = []
    add = False
    for line in text:
        if add:
            if 'Ångström' not in line: return rooms
            rooms.append(formatBooking(line))
        if not add and date in line:
            add = True

def getAvailableRooms(allRooms, allBookings, time): # returnerar lediga rum och nästa bokningstid
    bookedRooms = [booking[2] for booking in allBookings if booking[0] <= time < booking[1]]
    availableRooms = [room for room in allRooms if room not in bookedRooms]
    rooms = []
    for room in availableRooms:
        for booking in allBookings:
            if room == booking[2] and time < booking[0]:
                rooms.append([room, booking[0]])
                break
        else: # om det inte finns en nästa bokning, om den inte breakar
            rooms.append([room, 0])
    return rooms

 
url = r'https://cloud.timeedit.net/uu/web/schema/ri1Xc0gw8560YbQQY7ZgZZZX89ZZZX8Y0Cy300pZZZX8a5Y63Q562f5Y7ZZZZX881B6Cvy5G7Yv7yYYd5Yad7Y655agQ7.html'
allRooms = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 80412, 90402, 90403, 90409]
date = '2023-10-18'
time = 1630

soup = getSoup(url)
text = getBookingText(soup)
allBookings = getAllBookings(date, text)
available = getAvailableRooms(allRooms, allBookings, time)

print(available)
