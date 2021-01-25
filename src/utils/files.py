def url_to_path(url):
    """
    Turn URL (file://path/to/file) in regular file path (/path/to/file)
    """
    return url.replace("file://", "")