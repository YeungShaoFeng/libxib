from execjs import get as execjs_get
from time import ctime as t_ctime
from os import makedirs as make_dir

__APP_JS_PATH = "./js/app.js"
__APP_JS_ERROR_PATH = "../javascript/app.js"
DATA_ALBUMS = "./data/albums/"
UNKNOWN_ERROR = "unknown-error"
TIMED_OUT_TIME = 20
TIMED_OUT = "TIMED_OUT"
F_js_De = "De"
F_js_encode_url = "encode_url"
F_js_decode_url = "decode_url"

node = execjs_get()
ctx = None
try:
    with open(__APP_JS_PATH, "r", encoding="utf-8") as fp:
        ctx = node.compile(fp.read())
except FileNotFoundError:
    with open(__APP_JS_ERROR_PATH, 'r', encoding="utf-8") as fp:
        ctx = node.compile(fp.read())

_LoggerFlag = True
__LoggerFilePath = f"../data/log/{t_ctime()}.log"
make_dir('/'.join(__LoggerFilePath.split('/')[:-1]), exist_ok=True)
WriteLogToFile = False
if WriteLogToFile:
    with open(__LoggerFilePath, 'w', encoding='utf-8') as fp:
        fp.write(f"====== start time: [{t_ctime()}] =========\n")


def get_logger_file():
    return open(__LoggerFilePath, 'a+', encoding='utf-8')


def close_logger_file(logger_file_fp):
    logger_file_fp.close()


THE_URL = "https://girlimg.epio.app/api/articles?lang=en-us&filter={\"where\":{\"tag\":\"all\",\"lang\":\"en-us\"},\"limit\":20,\"skip\":"
__ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
__ACCEPT_ENCODING = "gzip,deflate,br"
__ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9,en;q=0.8,pl;q=0.7,de;q=0.6"
__CACHE_CONTROL = "max-age=0"
__CONNECTION = "keep-alive"
__SEC_FETCH_DEST = "document"
__SEC_FETCH_MODE = "navigate"
__SEC_FETCH_SITE = "none"
__SEC_FETCH_USER = "?1"
__UPGRADE_INSECURE_REQUESTS = "1"
__USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

page_headers = {
    "Accept": __ACCEPT,
    "Accept-Encoding": __ACCEPT_ENCODING,
    "Accept-Language": __ACCEPT_LANGUAGE,
    "Cache-Control": __CACHE_CONTROL,
    "Connection": __CONNECTION,
    "Host": "girlimg.epio.app",
    "Sec-Fetch-Dest": __SEC_FETCH_DEST,
    "Sec-Fetch-Mode": __SEC_FETCH_MODE,
    "Sec-Fetch-Site": __SEC_FETCH_SITE,
    "Sec-Fetch-User": __SEC_FETCH_USER,
    "Upgrade-Insecure-Requests": __UPGRADE_INSECURE_REQUESTS,
    "User-Agent": __USER_AGENT
}
album_headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Referer": None,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}
mypic_net_headers = {
    "accept": __ACCEPT,
    "accept-encoding": __ACCEPT_ENCODING,
    "accept-language": __ACCEPT_LANGUAGE,
    "cache-control": __CACHE_CONTROL,
    "sec-fetch-dest": __SEC_FETCH_DEST,
    "sec-fetch-mode": __SEC_FETCH_MODE,
    "sec-fetch-site": __SEC_FETCH_SITE,
    "sec-fetch-user": __SEC_FETCH_USER,
    "upgrade-insecure-requests": __UPGRADE_INSECURE_REQUESTS,
    "user-agent": __USER_AGENT
}
epio_headers = {
    "User-Agent": __USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us",
    "Connection": __CONNECTION,
    "Accept-Encoding": __ACCEPT_ENCODING,
    "Host": "cdn1-images.epio.app"
}
pic_headers = {
    "accept": __ACCEPT,
    "accept-encoding": __ACCEPT_ENCODING,
    "accept-language": __ACCEPT_LANGUAGE,
    "cache-control": __CACHE_CONTROL,
    "connection": __CONNECTION,
    "sec-fetch-dest": __SEC_FETCH_DEST,
    "sec-fetch-mode": __SEC_FETCH_MODE,
    "sec-fetch-site": __SEC_FETCH_SITE,
    "sec-fetch-user": __SEC_FETCH_USER,
    "upgrade-insecure-requests": __UPGRADE_INSECURE_REQUESTS,
    "Referer": "https://girlimg.epio.app/article/detail/{}",
    "user-agent": __USER_AGENT
}
