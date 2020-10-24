import csv
import os
import shutil
from pathlib import Path

VENTILATED = "ventilated"

NOT_VENTILATED = "not ventilated"

path_to_save: str = str(Path.home()) + os.path.sep + "Schreibtisch" + os.path.sep + "COVID-19-Data" + os.path.sep
path_to_sources: str = str(Path.home()) + os.path.sep + "Schreibtisch" + os.path.sep + "COVID-19-Data" + os.path.sep

path_to_sorted_sources: str = str(
    Path.home()) + os.path.sep + "Schreibtisch" + os.path.sep + "COVID-19-Data-Sorted" + os.path.sep

'''
Aggregates the COVID-19 data for germany from "Deutsche Interdisziplinäre Vereinigung für Intensiv- und Notfallmedizin"
It groups the data in a chunk of two weeks
'''

'''
These index declaration must not be used with non-ventilated-patient-data
'''
index_bundesland = 0
intex_gemeindeschluessel = 1
index_anzahl_meldebereiche = 2
index_faelle_covid_aktuell = 3
index_faelle_covid_aktuell_beatmet = 4
index_anzahl_standorte = 5
index_betten_frei = 6
index_betten_belegt = 7
index_daten_stand = 8


def main():
    source_files = []

    for root, dirs, files in os.walk(path_to_sources):
        for filename in files:
            source_files.append(path_to_sources + filename)

    os.makedirs(path_to_sorted_sources + VENTILATED, exist_ok=True)
    os.makedirs(path_to_sorted_sources + NOT_VENTILATED, exist_ok=True)

    for file in source_files:
        with open(file) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            for row in reader:
                if line_count == 0:
                    move_to_sorted_dir(file, row)
                    line_count = line_count + 1


def move_to_sorted_dir(file, row):
    """
    We need this differentiation, because the sourcedata differs.
    Some have the key for ventilated patients, some not.
    """
    if "faelle_covid_aktuell_beatmet" in row:
        shutil.move(file, path_to_sorted_sources + VENTILATED + os.path.sep)
    else:
        shutil.move(file, path_to_sorted_sources + NOT_VENTILATED + os.path.sep)


main()
