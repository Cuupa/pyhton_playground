import csv
import datetime
import os
import sys
from datetime import datetime
from threading import Timer

import requests

from CSVPriceextractor import CSVPriceextractor
from CommandLine import CommandLine
from Date import Date
from ValueExtractor import ValueExtractor

urls = [
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B075X181C5",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07GTSFS29",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07SNW9W48"
]

"""
    The values in the span-ids bellow are the final prices
"""
lookup_fields_final_price = ['newBuyBoxPrice', 'price_inside_buybox']
"""
    The values in the span-ids bellow are the 'original' prices, but stroked and followed by a 'save XY €! That's AB%!'
    Sort of...
    Will have the same value as the 'normal' price if not present
"""
lookup_fields_advertised_price = ['priceBlockStrikePriceString a-text-strike']

"""
    Lookup-Table for the Product-Name. The key is the product-id
"""
alias = {"B075X181C5": "Seagate Ironwolf 12 TB",
         "B07GTSFS29": "Seagate Ironwolf 14 TB",
         "B07SNW9W48": "Seagate Ironwolf 16 TB"}

row_names = ["Date", "Name", "Advertised Price", "Price"]


def main():
    path_to_save, urls_local, verbose, is_hourly = get_cmd_args(urls)
    process(path_to_save, urls_local, verbose, is_hourly)


def process(path_to_save, urls_local, verbose, is_hourly):
    if is_hourly:
        time = datetime.now()
        seconds = get_seconds_for_next_run(time)
        t = Timer(seconds, process, [path_to_save, urls_local, verbose, is_hourly])
        t.start()
        if verbose:
            print("Timer started")
    for url in urls_local:
        success, filepath = get_prices_write_to_csv(url, path_to_save, verbose)
        if success:
            lowest_price = CSVPriceextractor.get_lowest_price(get_filename(url, path_to_save))
            print("Price for " + get_message_text(url) + ": " + str(lowest_price))
    if verbose:
        print(str(datetime.now()) + ": executed")


def get_seconds_for_next_run(time):
    date = Date(time)
    scheduled_time = date.plus_hour(1)
    delta_t = scheduled_time - time
    return delta_t.total_seconds()


def get_cmd_args(urls_local):
    commandline = CommandLine(sys.argv)
    urls_commandline = commandline.get_urls()
    if urls_commandline is not None:
        urls_local = urls_commandline
    return commandline.get_path_to_save(), urls_local, commandline.is_verbose(), commandline.is_hourly()


def response_invalid(status_code, content):
    return status_code != 200 or str(content).find("<title dir=\"ltr\">Bot Check</title>") != -1


def get_prices_write_to_csv(url, path_to_save, verbose):
    try:
        response = requests.get(url, stream=False, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.108 Safari/537.36"})
        if response_invalid(response.status_code, response.content):
            print("Error getting result: HTTP/" + str(response.status_code))
        else:
            filepath = process_article(response, url, path_to_save, verbose)
        return True, filepath
    except:
        print("Unable to connect to " + url)
    return False, None


def process_article(response, url, path_to_save, verbose):
    try:
        advertised_price = ValueExtractor.get_value(response, 'span', lookup_fields_advertised_price)
        price = ValueExtractor.get_value(response, 'span', lookup_fields_final_price)
        if price is not None:
            if advertised_price is None:
                advertised_price = price
            path, name = os.path.split(url)
            filepath = get_and_create_file_path(name, path_to_save)
            if not os.path.exists(filepath):
                write_file_header(filepath, verbose)
            add_row(filepath, name, advertised_price, price, verbose)
            return filepath
        else:
            print("Error fetching price for " + url)
    except PermissionError:
        print("PermissionError")
        print(sys.exc_info()[0])
    except TypeError:
        print("TypeError")
        print(sys.exc_info()[0])
    return None


def add_row(filepath, name, advertised_price, price, verbose):
    csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
               escapechar='\\').writerow([datetime.now().date(), name, advertised_price, price])
    if verbose:
        print("Added to file " + os.path.abspath(filepath))


def write_file_header(filepath, verbose):
    csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
               escapechar='\\').writerow(row_names)
    if verbose:
        print("Created file " + os.path.abspath(filepath))


def get_and_create_file_path(name, path_to_save):
    filepath, filename = os.path.split(get_filename(name, path_to_save))
    if not os.path.exists(os.path.abspath(os.path.dirname(filename))):
        os.makedirs(os.path.abspath(os.path.dirname(filename)), exist_ok=True)
    if filepath != '':
        return filepath + os.path.sep + filename
    else:
        return filename


def get_filename(name, path_to_save):
    path, name = os.path.split(name)
    filename = alias.get(name) + ".csv"
    if path_to_save is None:
        return filename
    if not path_to_save.endswith(os.path.sep):
        return path_to_save + os.path.sep + filename
    else:
        return path_to_save + filename


def get_message_text(url):
    path, name = os.path.split(url)
    return alias.get(name)


main()
