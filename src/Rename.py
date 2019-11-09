import os
import re

dir = "path\\to\\dir"
dir_to_merge = "path\\to\\source"


def main():
    number_to_merge = get_numbers_to_merge()
    print(number_to_merge)

    for file in os.listdir(dir):
        path, filename = os.path.split(file)
        splitted = re.split(' - ', filename)
        new_number_string = get_leading_numbers(number_to_merge, splitted[0])

        new_file_name = new_number_string + ' - ' + splitted[1] + ' - ' + splitted[2]
        print(new_file_name)
        # os.rename(file, new_file_name)
        print(file)


def get_numbers_to_merge():
    number_to_merge = 0
    for file_to_merge in os.listdir(dir_to_merge):
        if file_to_merge.endswith('.mkv'):
            number_to_merge += 1
    return number_to_merge


def get_leading_numbers(number_to_merge, splitted_number):
    new_number = int(splitted_number) + number_to_merge
    new_number_string = ''
    if new_number < 99:
        new_number_string = '00' + str(new_number)

    elif new_number < 999:
        new_number_string = '0' + str(new_number)
    return new_number_string


main()
