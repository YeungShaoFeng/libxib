from requests import get as requests_get
from cfg import UNKNOWN_ERROR, TIMED_OUT, TIMED_OUT_TIME

try:
    from python.Logger import Logger
except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    from Logger import Logger


def get_this_url(_url: str, _headers: dict, text_mode=True):
    """
    :param _url: Target url
    :param _headers: Request headers
    :param text_mode: Return r.txt if set to True. Return r.content if set to False
    :return: {"content": error_msg if error occurs else r.text or r.content, "url": ...}
    """
    res = {"content": UNKNOWN_ERROR, "url": _url}
    try:
        r = requests_get(url=_url, headers=_headers)
        r.raise_for_status()
        # Logger.log([get_this_url, f'status_code: [{r.status_code}] | url: {_url}'])
        if text_mode:
            r.encoding = r.apparent_encoding
            res["content"] = r.text
        else:
            res["content"] = r.content
    except TimeoutError:
        Logger.log([get_this_url, f'{TimeoutError}: {url}'])
        res["content"] = TIMED_OUT
    finally:
        return res
