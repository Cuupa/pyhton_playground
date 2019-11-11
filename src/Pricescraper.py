import csv
import datetime
import os
import sys
from datetime import datetime
from threading import Timer

import requests

from CSVPriceextractor import CSVPriceextractor
from CommandLine import CommandLine
from ValueExtractor import ValueExtractor

urls = [
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B075X181C5",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07GTSFS29",
    "https://www.amazon.de/Seagate-ST4000VN008-IronWolf-interne-Festplatte/dp/B07SNW9W48"]

lookup_fields = ['newBuyBoxPrice', 'price_inside_buybox']

alias = {"B075X181C5": "Seagate Ironwolf 12 TB",
         "B07GTSFS29": "Seagate Ironwolf 14 TB",
         "B07SNW9W48": "Seagate Ironwolf 16 TB"}

row_names = ["Date, Name", "Price"]


def main():
    path_to_save, urls_local, verbose, is_hourly = get_cmd_args(urls)
    process(path_to_save, urls_local, verbose, is_hourly)


def process(path_to_save, urls_local, verbose, is_hourly):
    if is_hourly:
        time = datetime.now()
        scheduled_time = time.replace(day=time.day, hour=time.hour + 1, minute=time.minute, second=time.second,
                                      microsecond=time.microsecond)
        delta_t = scheduled_time - time
        seconds = delta_t.total_seconds()
        t = Timer(seconds, process)
        t.start()
        if verbose:
            print("Timer started")
    for url in urls_local:
        success = get_prices_write_to_csv(url, path_to_save, verbose)
        if success:
            lowest_price = CSVPriceextractor.get_lowest_price(get_filename(url, path_to_save))
            print("Price for " + get_message_text(url) + ": " + str(lowest_price))
    if verbose:
        print(str(datetime.now()) + ": executed")


def get_cmd_args(urls_local):
    commandline = CommandLine(sys.argv)
    urls_commandline = commandline.get_urls()
    if urls_commandline is not None:
        urls_local = urls_commandline
    return commandline.get_path_to_save(), urls_local, commandline.is_verbose(), commandline.is_hourly()


def get_prices_write_to_csv(url, path_to_save, verbose):
    try:
        request = requests.get(url, stream=False, headers={'User-agent': 'Mozilla/5.0'})
        if request.status_code != 200:
            print("Error getting result: HTTP/" + str(request.status_code))
        else:
            process_article(request, url, path_to_save, verbose)
            return True
    except:
        print("Unable to connect to " + url)
    return False


def process_article(request, url, path_to_save, verbose):
    try:
        price = ValueExtractor.get_value(request, 'span', lookup_fields)
        if price is not None:
            path, name = os.path.split(url)
            filepath = get_and_create_file_path(name, path_to_save)
            if not os.path.exists(filepath):
                write_file_header(filepath, verbose)
            add_row(filepath, name, price, verbose)
        else:
            print("Error fetching price for " + url)
    except PermissionError:
        print("PermissionError")
        print(sys.exc_info()[0])
    except TypeError:
        print("TypeError")
        print(sys.exc_info()[0])


def add_row(filepath, name, price, verbose):
    csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
               escapechar='\\').writerow([datetime.now().date(), name, price])
    if verbose:
        print("Added to file " + os.path.abspath(filepath))


def write_file_header(filepath, verbose):
    csv.writer(open(filepath, 'a', newline='\n'), quoting=csv.QUOTE_NONE, delimiter=';', quotechar='',
               escapechar='\\').writerow(row_names)
    if verbose:
        print("Created file " + os.path.abspath(filepath))


def get_and_create_file_path(name, path_to_save):
    filepath, filename = os.path.split(get_filename(name, path_to_save))
    if not os.path.exists(filepath):
        os.mkdirs(filepath)
    return filepath + os.path.sep + filename


def get_filename(name, path_to_save):
    path, name = os.path.split(name)
    filename = alias.get(name) + ".csv"
    if not path_to_save.endswith(os.path.sep):
        return path_to_save + os.path.sep + filename
    else:
        return path_to_save + filename


def get_message_text(url):
    path, name = os.path.split(url)
    return alias.get(name)


main()
