import requests
from bs4 import BeautifulSoup

def getSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, "html.parser")

def getText(soup):
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

def getBookings(date, time, text): # returnar bokade grupprum för datumet och tiden
    bookings = []
    add = False
    for line in text:
        if add:
            if 'Ångström' not in line:
                return bookings
            booking = formatBooking(line)
            if booking[0] <= time <= booking[1]:
                bookings.append(booking)
        if not add and date in line:
            add = True
        

url = r'https://cloud.timeedit.net/uu/web/schema/ri1X00gX8560Y8QQ8YZ985YY08y5009605X60Q560f543Z485694594558498050860560Y9554YYX8005878088Y84X086X96X506906X602008XY05166053991X50Y4295608635YY845695530YX5Y6755X6655X69X9856667X36Y65579955850995555Y036YX45605X9599057665X7856X535Y88079YY03Y2652X965665454525X936521Y050653569Y5060X35Y556X56XY6553963599Y4506X4650366951XY356069X50506692XY56069Y3656Y5X668915017805614Y8649Y7597X9066X4586555QY.html'
soup = getSoup(url)
text = getText(soup)

bookings = getBookings('2023-10-16', 1100, text)

print(bookings)