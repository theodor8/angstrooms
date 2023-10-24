import requests
from bs4 import BeautifulSoup

def getSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, "html.parser")

def getAllBookings(soup):
    table = soup.find('table', {'class' : 'restable'})
    rows = table.find_all('tr')
    rows = rows[2:]
    text = [ row.get_text() for row in rows ]
    text = [ x.split() for x in text ]
    return text

def formatTime(time): # '17:30' --> 1730
    return int(time[:2] + time[3:])

def formatRoom(room): # '10291,' --> 10291
    return int(room[:-1])

def formatBooking(booking):
    start = formatTime(booking[0])
    end = formatTime(booking[2])
    if 'Grupprum,' in booking: i = booking.index('Grupprum,') - 1
    else: i = booking.index('Bokningsbar') - 1
    room = formatRoom(booking[i])
    return [start, end, room]

def getDateBookings(date, bookings): # returnar alla bokningar för ett visst datum
    dateBookings = []
    add = False
    for booking in bookings:
        if add:
            if 'Ångström' not in booking: return dateBookings
            dateBookings.append(formatBooking(booking))
        if not add and date in booking:
            add = True

def getTimeBookings(time, bookings): # bokade rum på tiden
    return [booking for booking in bookings if booking[0] <= time < booking[1]]

def getNextBookingTime(bookings, room, time): # returnerar tiden för nästa bokning
    for booking in bookings:
        if room == booking[2] and time < booking[0]:
            return booking[0]
    return 0

def getAvailableRooms(allRooms, bookings): # returnerar lediga rum
    bookedRooms = [booking[2] for booking in bookings] # bara rummen
    availableRooms = [room for room in allRooms if room not in bookedRooms] # lediga rum på tiden
    return availableRooms

def available(url, allRooms, date, time):
    soup = getSoup(url)
    allBookings = getAllBookings(soup)
    dateBookings = getDateBookings(date, allBookings)
    timeBookings = getTimeBookings(time, dateBookings)
    availableRooms = getAvailableRooms(allRooms, timeBookings)
    result = []
    for room in availableRooms:
        nextBookingTime = getNextBookingTime(dateBookings, room, time)
        result.append([room, nextBookingTime])
    return result

 

url = r'https://cloud.timeedit.net/uu/web/schema/ri1Xc0gw8560YbQQY7ZgZZZX89ZZZX8Y0Cy300pZZZX8a5Y63Q562f5Y7ZZZZX881B6Cvy5G7Yv7yYYd5Yad7Y655agQ7.html'
allRooms = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 80412, 90402, 90403, 90409]
date = '2023-10-23'
time = 1630

print(available(url, allRooms, date, time))