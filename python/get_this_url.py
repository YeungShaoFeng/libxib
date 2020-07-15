from requests import get as requests_get


def get_this_url(url: str, headers: dict, text_mode=True):
    """
    :param url: Target url
    :param headers: Request headers
    :param text_mode: Return r.txt if set to True. Return r.content if set to False
    :return: r.txt(str) on success if text_mode set to True. |
             r.content(bin) on success if text_mode set to False. |
             r.status_code(int) on failure
    """
    r = None
    try:
        r = requests_get(url=url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except TimeoutError:
        print("Timed Out: " + url)
        return r.status_code
    finally:
        if r is None:
            return False
        return r.text if text_mode else r.content
