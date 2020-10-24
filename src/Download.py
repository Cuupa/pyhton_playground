import datetime
import os
import re
import shutil
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Download:

    def __init__(self, url, path_to_save, url_pattern, file_ending):
        self.url = url
        self.path_to_save = path_to_save
        self.url_pattern = url_pattern
        self.file_ending = file_ending

    def get_filename(self, pdf_element):
        link = self.get_final_link(pdf_element)
        response = requests.get(link, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        path, filename = os.path.split(link)

        filename = self.get_final_filename(filename)

        if self.path_to_save == '.':
            return filename, response
        return self.path_to_save + filename, response

    def get_final_link(self, pdf_element):
        link = pdf_element.get('href')
        if not str(link).startswith("http:") or not str(link).startswith("https:"):
            link = "https://" + parse.urlparse(self.url).hostname + link
        return link

    def get_final_filename(self, filename):
        if not self.file_ending in str(filename):
            filename = filename + self.file_ending
        return filename

    def download(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " HTTP/" + str(response.status_code))
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            found_elements = soup.find_all('a', attrs={'href': re.compile(self.url_pattern)})

            if not os.path.exists(self.path_to_save):
                os.makedirs(self.path_to_save)

            for element in found_elements:
                final_filename, response = self.get_filename(element)
                if not os.path.exists(final_filename):
                    with open(final_filename, 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
        print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + ": done step for url " + self.url)
