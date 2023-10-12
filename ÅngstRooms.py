from bs4 import BeautifulSoup
import requests


def getHtml(url):
    htmlDoc = requests.get(url)
    htmlString = BeautifulSoup(htmlDoc.content, features="html.parser")
    return htmlString

def getBookings(html):
    objects = html.find_all('tr', {'class' : 'rr clickable2'})
    bookings = [ x.get_text() for x in objects ]
    return bookings


html = getHtml("https://cloud.timeedit.net/uu/web/schema/ri1XZ0g78560Y7QQ8YZ985QY0yy500Q6c5a60Q560f54nZh8xlb6dp_xllybaxw_nrxdj.html")
bookings = getBookings(html)
print(bookings[2])
