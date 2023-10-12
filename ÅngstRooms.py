from bs4 import BeautifulSoup
import requests


def getHtml(url):
    htmlDoc = requests.get(url)
    htmlString = BeautifulSoup(htmlDoc.content, features="html.parser")
    return htmlString


html = getHtml("https://cloud.timeedit.net/uu/web/schema/ri1X300ZZ9005QQQ0fZ67o6Y00yQ5YcfYQ0f7Y662v5QX109Y7ZZ0_hapQjxxy_ncdlllyrxwbnaxdb.html")
print(html.prettify("utf-8"))
