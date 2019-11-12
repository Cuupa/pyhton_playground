import datetime
import os
import re
import shutil

import requests
from bs4 import BeautifulSoup


class Download:

    def __init__(self, url, download_url, path_to_save, url_pattern):
        self.url = url
        self.download_url = download_url
        self.path_to_save = path_to_save
        self.url_pattern = url_pattern

    def get_filename(self, pdf_element):
        link = pdf_element.get('href')
        response = requests.get(link, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        path, filename = os.path.split(link)
        if self.path_to_save == '.':
            return filename, response
        return self.path_to_save + filename, response

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
