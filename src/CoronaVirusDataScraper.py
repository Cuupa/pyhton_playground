import os
from pathlib import Path

import numpy as np

from src.Download import Download

url: str = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={0}"
url_pattern_csv: str = "^(\\/divi-intensivregister-tagesreport-archiv-csv\\/divi-intensivregister-[2]{1}[0]{1}[2]{1}[0-9]{1}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}\\/viewdocument\\/[0-9]{4})"
file_ending: str = ".csv"

path_to_save: str = str(Path.home()) + os.path.sep + "Schreibtisch" + os.path.sep + "COVID-19-Data" + os.path.sep

'''
Downloads the COVID-19 data for germany from "Deutsche Interdisziplinäre Vereinigung für Intensiv- und Notfallmedizin"
'''


def main():
    for page_index in np.arange(10, 200, 10):
        Download(url.format(str(page_index)), path_to_save, url_pattern_csv, file_ending).download()


main()
