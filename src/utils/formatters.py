def format_file_size(bytes, suffix='B'):
    """
    Get file size in human readable format
    """
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(bytes) < 1000.0:
            return "%3.2f%s%s" % (bytes, unit, suffix)
        bytes /= 1000.0

    return "%.1f%s%s" % (bytes, 'Y', suffix)
