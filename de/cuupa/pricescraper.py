import csv
import os
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

path_to_save = None


def is_lowes_price(url):
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


def print_help():
    print("--help\t\t\t\t\tPrints this screen.")
    print("--url=www.amazon.com/product_id\t\tThe url which shall be processed")
    print("\t\t\t\t\tIf no url is specified, the program will use the hardcoded ones.")
    print("--out=/path/to/save/to\t\t\tThe directory to save to. If the directory doesn\'t exist it will be created.")
    print("\t\t\t\t\tIf no output directory is specified, the files will be saved next to the program.")
    exit()


def parse_command_line_arguments(args):
    if "--help" in args:
        print_help()

    if "--out=" in args:
        handle_out_arg(args)

    if "--url=" in args:
        handle_url_arg(args)


def handle_url_arg(args):
    urls_arg = args.split("=")
    if len(urls_arg) == 2:
        urls = urls_arg[1]
    else:
        print_help()
        exit()


def handle_out_arg(args):
    out_arg = args.split("=")
    if len(out_arg) == 2:
        path_to_save = out_arg[1]
    else:
        print_help()
        exit()


def main():
    for args in sys.argv[1::]:
        parse_command_line_arguments(args)

    for url in urls:
        get_prices_write_to_csv(url)
        is_lowered, price = is_lowes_price(url)
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

        if not os.path.exists(filename):
            csv.writer(open(filename, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                       escapechar='\\').writerow(row_names)
            print("Created file " + os.path.abspath(filename))

        csv.writer(open(filename, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
                   escapechar='\\').writerow([name, final_price])
        print("Added to file " + os.path.abspath(filename))
    except:
        print(sys.exc_info()[0])


def get_filename(name):
    if path_to_save is None:
        filename = alias.get(name) + '.csv'
    else:
        if not path_to_save.endswith('/') or not path_to_save.endswith('\\'):
            filename = path_to_save + '/'
    return filename


def get_price(request):
    soup = BeautifulSoup(request.content, 'html.parser')
    element_price = soup.find("span", id="newBuyBoxPrice")
    if element_price is None:
        element_price = soup.find("span", id="price_inside_buybox")
    return element_price.text.strip()


main()
