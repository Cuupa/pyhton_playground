import os
import sys
from os import walk, path, makedirs, rename, rmdir, remove

"""
Import Win32 API when whe're using windows
"""
if os.name == "nt":
    import win32api, win32con

images_endings = [".jpg", ".jpeg", ".png", ".heic"]
video_endings = [".mp4", ".avi", ".mkv", ".heif"]
iso_endings = [".iso", ".img"]
archive_endings = [".zip", ".tar", ".gz", ".tar.gz", ".7z", ".rar", ".xz", ".tar.xz", ".tgz"]
executable_endings = [".exe", ".java", ".py", ".sh", ".bat"]
ebook_endings = [".epub", ".mobi"]
audio_endings = [".aac", ".mid", ".ogg", ".mp3", ".wav"]
office_endings = [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]
non_processing_endings = [".lnk", ".crdownload", ".db", ""]


def check_for_ebooks(file, files):
    other_files = []
    for file_ in files:
        filename_to_check, ending_to_check = path.splitext(file_)
        filename, ending = path.splitext(file)
        if filename_to_check == filename and ending != ending_to_check:
            if file not in other_files:
                other_files.append(file)
            if file_ not in other_files:
                other_files.append(file_)
    return other_files


def try_move(source, destination):
    try:
        rename(source, destination)
    except:
        print("Unable to move file ${0}".format(source))


def try_remove(file):
    try:
        remove(file)
    except:
        print("Unable to remove file ${0}".format(file))


def move_files_to(path_to_sort, file, folder):
    target_dir = path_to_sort + folder
    create_directory_if_not_exists(path_to_sort, folder)
    final_filename = target_dir + path.sep + file
    if not path.exists(final_filename):
        try_move(path_to_sort + file, final_filename)
    else:
        try_remove(path_to_sort + file)


def handle(path_to_sort, endings, foldername):
    files = get_files(path_to_sort)
    for file in files:
        filename, ending = path.splitext(file)
        if ending in non_processing_endings:
            print("Ignoring ${0}".format(file))
            return
        if ending in endings:
            move_files_to(path_to_sort, file, foldername)


def handle_remaining(path_to_sort):
    files = get_files(path_to_sort)
    for file in files:
        filename, ending = path.splitext(file)
        if ending in non_processing_endings:
            print("Ignoring ${0}".format(file))
            continue
        move_files_to(path_to_sort, file, ending.upper().replace('.', ''))


def handle_ebooks(path_to_sort, path_to_ebooks):
    files = get_files(path_to_sort)

    for file in files:
        filename, ending = path.splitext(file)
        if ending == ".pdf":
            other_files = check_for_ebooks(file, files)
            move_files_to_ebooks(path_to_sort, other_files, path_to_ebooks)

    files = get_files(path_to_sort)

    for file in files:
        filename, ending = path.splitext(file)
        if ending in ebook_endings:
            move_files_to(path_to_sort, file, 'ebooks' + path.sep + filename)


def file_is_hidden(file):
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(file)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return file.startswith('.')


def get_files(path_to_sort):
    files = []
    for (_, _, filenames) in walk(path_to_sort):
        files = filenames
        break
    value = []
    for file in files:
        if not file_is_hidden(file):
            value.append(file)
    return value


def move_files_to_ebooks(path_to_sort, other_files, path_to_ebooks):
    for file_to_move in other_files:
        filename, ending = path.splitext(file_to_move)
        create_directory_if_not_exists(path_to_ebooks, filename)
        final_filename = path_to_ebooks + filename + path.sep + filename + ending
        if not path.exists(final_filename):
            rename(path_to_sort + file_to_move, final_filename)
        else:
            remove(path_to_sort + file_to_move)


def create_directory_if_not_exists(dir, subfolder):
    if not path.exists(dir + subfolder):
        makedirs(dir + subfolder)


def handle_empty_dirs(path):
    directories = []
    for (_, directory_names, _) in walk(path):
        directories = directory_names
        break
    for directory in directories:
        try:
            rmdir(path + directory)
        except:
            print("Skipping non empty directory ${0}".format(path + directory))


def run():
    if len(sys.argv) < 2:
        print("No path to sort provided")
        return
    path_to_sort = sys.argv[1]
    if not path_to_sort.endswith(path.sep):
        path_to_sort = path_to_sort + path.sep
    print("Sorting directory ${0}".format(path_to_sort))

    handle_ebooks(path_to_sort, path_to_sort + 'ebooks' + path.sep)
    handle(path_to_sort, iso_endings, 'ISOs')
    handle(path_to_sort, ebook_endings, 'ebooks')
    handle(path_to_sort, images_endings, 'Images')
    handle(path_to_sort, video_endings, 'Videos')
    handle(path_to_sort, archive_endings, 'Archives')
    handle(path_to_sort, audio_endings, 'Audio')
    handle(path_to_sort, executable_endings, 'Programs')
    handle(path_to_sort, office_endings, 'Office Documents')
    handle_remaining(path_to_sort)
    handle_empty_dirs(path_to_sort)


run()
