import os
from pathlib import Path
from urllib.parse import urlparse

def url_to_path(url):
    path = urlparse(url).path
    if os.name == 'nt':
        path = path.replace('/', '', 1)

    return str(Path(path))

def open_torrent_file(url):
    print(url_to_path(url))
    return open(url_to_path(url), 'rb')
