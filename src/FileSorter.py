import sys
from os import walk, path, makedirs, rename

images_endings = [".jpg", ".jpeg", ".png", ".heic"]
video_endings = [".mp4", ".avi", ".mkv", ".heif"]
iso_endings = [".iso", ".img"]
archive_endings = [".zip", ".tar", ".gz", ".tar.gz", ".7z", ".rar", ".xz", ".tar.xz", ".tgz"]
executable_endings = [".exe", ".java", ".py"]
ebook_endings = [".epub", '.mobi']
audio_endings = [".aac", ".mid", ".ogg", ".mp3", ".wav"]


def check_for_ebooks(file, files):
    other_files = []
    for file_ in files:
        filename_to_check, ending_to_check = path.splitext(file_)
        filename, ending = path.splitext(file)
        if filename_to_check == filename and ending != ending_to_check and ending_to_check in ebook_endings:
            other_files.append(file)
            other_files.append(file_)
    return other_files


def move_files_to(path_to_sort, file, folder):
    target_dir = path_to_sort + folder
    create_directory_if_not_exists(path_to_sort, folder)
    rename(path_to_sort + file, target_dir + '/' + file)
    pass


def handle(path_to_sort, endings, foldername):
    files = []
    for (_, _, filenames) in walk(path_to_sort):
        files = filenames
        break
    for file in files:
        filename, ending = path.splitext(file)
        if ending == '.crdownload':
            return
        if ending in endings:
            move_files_to(path_to_sort, file, foldername)


def handle_remaining(path_to_sort):
    files = []
    for (_, _, filenames) in walk(path_to_sort):
        files = filenames
        break
    for file in files:
        filename, ending = path.splitext(file)
        move_files_to(path_to_sort, file, ending.upper().replace('.', ''))


def handle_ebooks(path_to_sort, path_to_ebooks):
    files = []
    for (_, _, filenames) in walk(path_to_sort):
        files = filenames
        break

    for file in files:
        filename, ending = path.splitext(file)
        if ending == ".pdf":
            other_files = check_for_ebooks(file, files)
            move_files_to_ebooks(path_to_sort, other_files, path_to_ebooks)


def move_files_to_ebooks(path_to_sort, other_files, path_to_ebooks):
    for file_to_move in other_files:
        filename, ending = path.splitext(file_to_move)
        create_directory_if_not_exists(path_to_ebooks, filename)
        rename(path_to_sort + file_to_move, path_to_ebooks + filename + '/' + filename + ending)


def create_directory_if_not_exists(dir, subfolder):
    if not path.exists(dir + subfolder):
        makedirs(dir + subfolder)


def run():
    if len(sys.argv) < 2:
        print("No path to sort provided")
        return
    path_to_sort = sys.argv[1]
    if not path_to_sort.endswith('/'):
        path_to_sort = path_to_sort + '/'
    print("Sorting directory ${0}".format(path_to_sort))

    handle_ebooks(path_to_sort, path_to_sort + '/ebooks/')
    handle(path_to_sort, iso_endings, 'ISOs')
    handle(path_to_sort, ebook_endings, 'ebooks')
    handle(path_to_sort, images_endings, 'Images')
    handle(path_to_sort, video_endings, 'Videos')
    handle(path_to_sort, archive_endings, 'Archives')
    handle(path_to_sort, audio_endings, 'Audio')
    handle(path_to_sort, executable_endings, 'Programs')
    handle_remaining(path_to_sort)


run()
