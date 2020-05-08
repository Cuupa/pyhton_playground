import hashlib
import os
import subprocess

PATH = "/path/to/images/"

path_to_checksum_filer = "checksum"
user = "simon.thiel"
checksum_file = "checksum.txt"

programName = "guetzli"
parameterQuality = "--quality"
quality100 = "100"
paramerterLoggingVerbose = "--verbose"

COMPRESSED_JPG = '_compressed.jpg'
JPG = '.jpg'

BUFFER_SIZE: int = 65536

sha1 = hashlib.sha1()


def calculate_hash(file):
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def list_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.jpg' in file or 'jpeg' in file:
                files.append(os.path.join(r, file))
    return files


def write_checksum(hash_new_file):
    f = open(path_to_checksum_filer + "/" + user + "/" + checksum_file, "a")
    f.writelines(hash_new_file + '\n')
    f.close()


def create_checksum_file():
    if not os.path.exists(path_to_checksum_filer):
        os.mkdir(path_to_checksum_filer)
    if not os.path.exists(path_to_checksum_filer + "/" + user):
        os.mkdir(path_to_checksum_filer + "/" + user)
    if not os.path.exists(path_to_checksum_filer + "/" + user + "/" + checksum_file):
        f = open(path_to_checksum_filer + "/" + user + "/" + checksum_file, "w+")
        f.close()


def check_checksum(hash_original):
    f = open(path_to_checksum_filer + "/" + user + "/" + checksum_file, "r")
    lines = f.readlines()
    for line in lines:
        if line.replace('\n', '') == hash_original:
            return True
    return False


def main():
    files = list_files(PATH)
    create_checksum_file()

    overall_filesize = 0
    overall_filesize_new = 0

    for file in files:
        original_file_size = os.stat(file).st_size
        overall_filesize = overall_filesize + original_file_size
        hash_original = calculate_hash(file)
        is_already_compressed = check_checksum(hash_original)

        if is_already_compressed:
            continue

        hash_new_file: str
        new_filename = file.replace(JPG, COMPRESSED_JPG)
        subprocess.call([programName, parameterQuality, quality100, paramerterLoggingVerbose, file, new_filename])
        new_filesize = os.stat(new_filename).st_size
        overall_filesize_new = new_filesize + overall_filesize_new
        if new_filesize < original_file_size:
            hash_new_file = calculate_hash(new_filename)
            os.remove(file)
            os.rename(new_filename, new_filename.replace(COMPRESSED_JPG, JPG))
        else:
            os.remove(new_filename)
            hash_new_file = hash_original

        if hash_new_file is not None and hash_new_file is not "":
            write_checksum(hash_new_file)
            hash_new_file = ""

    print("Original file size: " + overall_filesize)
    print("File size after processing: " + overall_filesize_new)


main()
