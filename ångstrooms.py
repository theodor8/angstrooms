import requests
from bs4 import BeautifulSoup

def getSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, "html.parser")

def getAllBookings(soup): # tar text från soup och returnerar alla rader på sidan i form av en lista(bokningarna)
    table = soup.find('table', {'class' : 'restable'})
    rows = table.find_all('tr')
    rows = rows[2:]
    text = [ row.get_text() for row in rows ]
    text = [ x.split() for x in text ]
    return text

def formatTime(time): # '17:30' --> 1730
    return int(time[:2] + time[3:])

def formatRoom(room): # '10291,' --> 10291
    return int(room[:-1]) # tar bort kommat och gör till heltal


# ['10:15', '-', '12:00', 'Energieffektivisering', 'i', 'byggnader', 'BI3', '101154,', 'Grupprum,', 'Ångström', 'Presentation', 'Annica', 'Nilsson', 'Karta']
def formatBooking(booking):# formaterar en bokningslista
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

    # gör flera bokningar om det finns fler rum
    # [1300, 1400, [10210, 10221]] --> [1300, 1400, 10210], [1300, 1400, 10221]
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
    availableRooms = [room for room in allRooms if room not in bookedRooms] # lediga rum på tiden, varje rum om rummet inte är bokat
    return availableRooms

def available(url, allRooms, date, time):
    soup = getSoup(url)
    allBookings = getAllBookings(soup)
    dateBookings = getDateBookings(date, allBookings)
    timeBookings = getTimeBookings(time, dateBookings)
    availableRooms = getAvailableRooms(allRooms, timeBookings)

    # lägger till nästa bokningstid
    result = []
    for room in availableRooms:
        nextBookingTime = getNextBookingTime(dateBookings, room, time)
        result.append([room, nextBookingTime])
        
    return result

 

url = r'https://cloud.timeedit.net/uu/web/schema/ri17Y664205004QQ89Z5509005y0Y0886g46g5X6Y65ZX856088Q0850085866063860XY980059945YY05X96579554YX84X840Y88Y6485XY654X6050850628X30Y955198556609X15902006YX3599555768054663500685536Y9766X750959Y55X9Y5XY66X3595X936587Y055658569Y7066X25Y559X66XY65536695890752Y539669555Y05096062X5Y4Y450X9553963X5206X56531X50Y63560Y6664953X605Y6629Y9565063X56Y55X6505X03664159Y577Y585598Q54996X15nY8h160X7YZ6d9051086X6y6c4lQa4x_nrxldjp_xwbbaxly.html'
allRooms = [101154, 101156, 101168, 101170, 101174, 101180, 101182, 101192, 10131, 10133, 10205, 10207, 10208, 10210, 10211, 10212, 10213, 10214, 10215, 1403, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 80412, 90402, 90403, 90409]
date = '2023-10-27'
time = 1315

print(available(url, allRooms, date, time))