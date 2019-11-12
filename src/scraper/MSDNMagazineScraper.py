import os

from util.Download import Download

url: str = "https://docs.microsoft.com/en-us/archive/msdn-magazine/msdn-magazine-issues"
download_url: str = "http://download.microsoft.com/download/"
url_pattern: str = "^(http:\\/\\/download.microsoft.com\\/download[\\/0-9a-f\\-]*[pdf]{1})"
path_to_save: str = os.path.curdir + "download" + os.path.sep


def main():
    Download(url, download_url, path_to_save, url_pattern).download()


main()
