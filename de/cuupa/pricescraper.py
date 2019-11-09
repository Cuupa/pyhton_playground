import os

import csv
import sys

import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B075X181C5",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07GTSFS29",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07SNW9W48"]

alias = {"B075X181C5": "Seagate Ironwolf 12 TB",
         "B07GTSFS29": "Seagate Ironwolf 14 TB",
         "B07SNW9W48": "Seagate Ironwolf 16 TB"}

row_names = ["Name", "Price"]


def main():
    for url in urls:
        request = requests.get(url, stream=False, headers={'User-agent': 'Mozilla/5.0'})
        print(request.cookies)
        for i in request.cookies:
            print(i)
        if request.status_code != 200:
            print("Error getting result")
        else:
            process_article(request, url)


def process_article(request, url):
    try:
        final_price = get_price(request)
        path, name = os.path.split(url)
        filename = alias.get(name) + '.csv'
        if not os.path.exists(filename):
            csv.writer(open(filename, 'a', newline=''), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                       escapechar='\\').writerow(row_names)

        csv.writer(open(filename, 'a', newline=''), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                   escapechar='\\').writerow([name, final_price])

    except:
        print(sys.exc_info()[0])


def get_price(request):
    soup = BeautifulSoup(request.content, 'html.parser')
    element_price = soup.find("span", id="newBuyBoxPrice")
    if element_price is None:
        element_price = soup.find("span", id="price_inside_buybox")
    return element_price.text.strip()


main()
