import os

from src.Download import Download

url: str = "https://docs.microsoft.com/en-us/archive/msdn-magazine/msdn-magazine-issues"
download_url: str = "http://download.microsoft.com/download/"
url_pattern_PDFs: str = "^(http:\\/\\/download.microsoft.com\\/download[\\/0-9a-f\\-]*[pdf]{1})"
url_pattern_CHMs: str = "^(http:\\/\\/download.microsoft.com\\/download[\\/0-9a-f\\-]*[chm]{1})"
path_to_save: str = os.path.curdir + "download" + os.path.sep


def main():
    Download(url, download_url, path_to_save, url_pattern_PDFs).download()
    Download(url, download_url, path_to_save, url_pattern_CHMs).download()


main()
