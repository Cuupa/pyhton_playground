import csv
import datetime
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

row_names = ["Date, Name", "Price"]


def is_lowest_price(url, path_to_save):
    path, name = os.path.split(url)
    filename = get_filename(name, path_to_save)
    with open(filename, 'r', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        lowest_price = float('inf')
        list_prices = list()
        length = 0
        for row in reader:
            if row[1] != 'Price':
                length += 1
                price = float(row[2].split()[0].replace(',', '.'))
                list_prices.append(price)
                if price < lowest_price:
                    lowest_price = price

        if list_prices[length - 1] == lowest_price:
            return True, lowest_price
    return False, float('inf')


def get_message_text(url):
    path, name = os.path.split(url)
    return alias.get(name)


def main():
    path_to_save, urls_local, verbose = get_cmd_args(urls)
    if urls_local is None:
        urls_local = urls

    for url in urls_local:
        get_prices_write_to_csv(url, path_to_save, verbose)
        is_lowered, price = is_lowest_price(url, path_to_save)
        if is_lowered:
            print("Price dropped for " + get_message_text(url) + " " + str(price))


def get_cmd_args(urls_local):
    for args in sys.argv[2::]:
        commandline = CommandLine(args)
        path_to_save = commandline.get_path_to_save()
        urls_commandline = commandline.get_urls()
        if urls_commandline is not None:
            urls_local = urls_commandline
        verbose = commandline.is_verbose()
        return path_to_save, urls_local, verbose
    return None, None, False


def get_prices_write_to_csv(url, path_to_save, verbose):
    request = requests.get(url, stream=False, headers={'User-agent': 'Mozilla/5.0'})
    if request.status_code != 200:
        print("Error getting result: HTTP/" + str(request.status_code))
    else:
        process_article(request, url, path_to_save, verbose)


def process_article(request, url, path_to_save, verbose):
    try:
        price = get_price(request)
        path, name = os.path.split(url)
        filepath = get_and_create_file_path(name, path_to_save)
        if not os.path.exists(filepath):
            csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                       escapechar='\\').writerow(row_names)
            if verbose:
                print("Created file " + os.path.abspath(filepath))

        csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                   escapechar='\\').writerow([datetime.datetime.now().date(), name, price])
        if verbose:
            print("Added to file " + os.path.abspath(filepath))
    except PermissionError:
        print("PermissionError")
        print(sys.exc_info()[0])
    except TypeError:
        print("TypeError")
        print(sys.exc_info()[0])


def get_and_create_file_path(name, path_to_save):
    filepath, filename = os.path.split(get_filename(name, path_to_save))
    if not os.path.exists(filepath) and '' not in filepath:
        os.mkdirs(filepath)
    return filepath + os.path.sep + filename


def get_filename(name, path_to_save):
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
