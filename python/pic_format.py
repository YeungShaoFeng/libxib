def pic_format(file_head: bin):
    """
    Determine the format of a picture. \n
    :param file_head: The [:8] of the pic's file_head.
    :return: Pic's format if matched, "unknown" if none matched .
    """
    res = "unknown"
    if b'\xff\xd8\xff' in file_head:
        res = 'jpg'
    elif b'\x89PNG\r\n\x1a\n' in file_head:
        res = 'png'

    return res
