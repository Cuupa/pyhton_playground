import csv


class CSVPriceextractor:

    def __init__(self):
        pass

    @staticmethod
    def get_lowest_price(filename):
        try:
            with open(filename, 'r', newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                lowest_price = float('inf')
                list_prices = list()
                length = 0
                for row in reader:
                    if row[3] != 'Price':
                        length += 1
                        price = float(row[3].split()[0].replace(',', '.'))
                        list_prices.append(price)
                        if price < lowest_price:
                            lowest_price = price
                return lowest_price
        except FileNotFoundError:
            print("File " + filename + " not existing")
            return float('inf')

    @staticmethod
    def get_highest_price(filename):
        with open(filename, 'r', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            highest_price = float(0)
            list_prices = list()
            length = 0
            for row in reader:
                if row[1] != 'Price':
                    length += 1
                    price = float(row[2].split()[0].replace(',', '.'))
                    list_prices.append(price)
                    if price > highest_price:
                        highest_price = price
            return highest_price
