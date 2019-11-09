import csv
import os
import sys

import requests
from bs4 import BeautifulSoup

from CommandLine import CommandLine

urls = [
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B075X181C5",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07GTSFS29",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07SNW9W48"]

alias = {"B075X181C5": "Seagate Ironwolf 12 TB",
         "B07GTSFS29": "Seagate Ironwolf 14 TB",
         "B07SNW9W48": "Seagate Ironwolf 16 TB"}

row_names = ["Name", "Price"]

path_to_save = None


def is_lowest_price(url):
    path, name = os.path.split(url)
    filename = alias.get(name) + '.csv'
    with open(filename, 'r', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        lowest_price = float('inf')
        list_prices = list()
        length = 0
        for row in reader:
            if row[1] != 'Price':
                length += 1
                price = float(row[1].split()[0].replace(',', '.'))
                list_prices.append(price)
                if price < lowest_price:
                    lowest_price = price

        if list_prices[length - 1] == lowest_price:
            return True, lowest_price
    return False, float(0)


def get_message_text(url):
    path, name = os.path.split(url)
    return alias.get(name)


def main():
    for args in sys.argv[1::]:
        CommandLine(args)

    for url in urls:
        get_prices_write_to_csv(url)
        is_lowered, price = is_lowest_price(url)
        if is_lowered:
            print("Price dropped for " + get_message_text(url) + " " + str(price))


def get_prices_write_to_csv(url):
    request = requests.get(url, stream=False, headers={'User-agent': 'Mozilla/5.0'})
    if request.status_code != 200:
        print("Error getting result: HTTP/" + str(request.status_code))
    else:
        process_article(request, url)


def process_article(request, url):
    try:
        final_price = get_price(request)
        path, name = os.path.split(url)
        filepath, filename = os.path.split(get_filename(name))
        if not os.path.exists(filepath) and '' not in filepath:
            os.mkdirs(filepath)

        final_filepath = filepath + os.path.sep + filename
        if not os.path.exists(final_filepath):
            csv.writer(open(final_filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                       escapechar='\\').writerow(row_names)
            print("Created file " + os.path.abspath(filename))

        csv.writer(open(final_filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                   escapechar='\\').writerow([name, final_price])
        print("Added to file " + os.path.abspath(final_filepath))
    except:
        print(sys.exc_info()[0])


def get_filename(name):
    filename = alias.get(name) + ".csv"
    if path_to_save is not None:
        if not path_to_save.endswith(os.path.sep):
            return path_to_save + os.path.sep + filename
        else:
            return path_to_save + filename
    return filename


def get_price(request):
    soup = BeautifulSoup(request.content, 'html.parser')
    element_price = soup.find("span", id="newBuyBoxPrice")
    if element_price is None:
        element_price = soup.find("span", id="price_inside_buybox")
    return element_price.text.strip()


main()
