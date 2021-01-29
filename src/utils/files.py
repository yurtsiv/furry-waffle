import os
from pathlib import Path
from urllib.parse import urlparse

def url_to_path(url):
    path = urlparse(url).path.replace('/', '', 1)
    return str(Path(path))

def open_torrent_file(url):
    return open(url_to_path(url), 'rb')
