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
    rooms = []
    if 'Grupprum,' in booking:
        for i, word in enumerate(booking):
            if word == 'Grupprum,':
                rooms.append(formatRoom(booking[i - 1]))
    elif 'Bokningsbar' in booking:
        for i, word in enumerate(booking):
            if word == 'Bokningsbar':
                rooms.append(formatRoom(booking[i - 1]))
    return [start, end, rooms]

def getDateBookings(date, bookings): # returnar alla bokningar för ett visst datum
    dateBookings = []
    add = False
    for booking in bookings:
        if add:
            if 'Ångström' not in booking: break
            dateBookings.append(formatBooking(booking))
        if not add and date in booking:
            add = True

    dateBookingsNew = []
    for booking in dateBookings:
        start = booking[0]
        end = booking[1]
        rooms = booking[2]
        for room in rooms:
            dateBookingsNew.append([start, end, room])

    return dateBookingsNew

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

 

url = r'https://cloud.timeedit.net/uu/web/schema/ri1X00gX8560Y8QQ8YZ985YY08y5009605X60Q560f543Z485694594558498050860560Y9554YYX8005878088Y84X086X96X506906X602008XY05166053991X50Y4295608635YY845695530YX5Y6755X6655X69X9856667X36Y65579955850995555Y036YX45605X9599057665X7856X535Y88079YY03Y2652X965665454525X936521Y050653569Y5060X35Y556X56XY6553963599Y4506X4650366951XY356069X50506692XY56069Y3656Y5X668915017805614Y8649Y7597X9066X4586555QY.html'
allRooms = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 80412, 90402, 90403, 90409]
date = '2023-10-24'
time = 1315

print(available(url, allRooms, date, time))