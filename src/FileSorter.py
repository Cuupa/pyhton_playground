import sys
from os import walk, path, makedirs, rename, rmdir, remove

images_endings = [".jpg", ".jpeg", ".png", ".heic"]
video_endings = [".mp4", ".avi", ".mkv", ".heif"]
iso_endings = [".iso", ".img"]
archive_endings = [".zip", ".tar", ".gz", ".tar.gz", ".7z", ".rar", ".xz", ".tar.xz", ".tgz"]
executable_endings = [".exe", ".java", ".py", ".sh", ".bat"]
ebook_endings = [".epub", ".mobi"]
audio_endings = [".aac", ".mid", ".ogg", ".mp3", ".wav"]
office_endings = [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]


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


def move_files_to(path_to_sort, file, folder):
    target_dir = path_to_sort + folder
    create_directory_if_not_exists(path_to_sort, folder)
    final_filename = target_dir + '/' + file
    if not path.exists(final_filename):
        rename(path_to_sort + file, final_filename)
    else:
        remove(path_to_sort + file)


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
        if ending == '.crdownload' or ending == '':
            continue
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

    for (_, _, filenames) in walk(path_to_sort):
        files = filenames
        break
    for file in files:
        filename, ending = path.splitext(file)
        if ending in ebook_endings:
            move_files_to(path_to_sort, file, 'ebooks/' + filename)


def move_files_to_ebooks(path_to_sort, other_files, path_to_ebooks):
    for file_to_move in other_files:
        filename, ending = path.splitext(file_to_move)
        create_directory_if_not_exists(path_to_ebooks, filename)
        final_filename = path_to_ebooks + filename + '/' + filename + ending
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
    if not path_to_sort.endswith('/'):
        path_to_sort = path_to_sort + '/'
    print("Sorting directory ${0}".format(path_to_sort))

    handle_ebooks(path_to_sort, path_to_sort + 'ebooks/')
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
