from python.get_this_url import get_this_url
from python.make_dir import make_dir
from multiprocessing import Process, Pool


def saver(msg: dict):
    # print("----callback func --pid=%d" % os.getpid())
    saving_path = msg["saving_path"]
    content_name = '/'.join(saving_path.split("/")[-2:])
    print(f"Saving {content_name} to {saving_path}...", end='')
    parent_dir = '/'.join(saving_path.split('/')[:-1])
    make_dir(parent_dir)
    with open(saving_path, "w", encoding="utf-8") as fp:
        fp.write(str(msg["content"]))
    print("Done. ")


def get(url, headers):
    print(f"Getting '{url}' with '{headers}'... ", end='')
    print("Done")
    return url


def img_dl_step(url_dict: dict, headers: dict) -> dict:
    """
    A step of img_dl. \n
    :param url_dict: A dict consists of "content_name", "saving_path".
    :param headers: requests headers.
    :return: Downloaded content.
    """
    # print("pid: {}, ppid: {}".format(os.getpid(), os.getppid()))
    # content = get_this_url(url_dict["url"], headers, text_mode=False)
    content = get(url_dict["url"], headers)
    return {"content": content, "saving_path": url_dict["saving_path"]}


def img_dl(thread_num: int, url_list: list, headers: dict):
    """
    A downloader for img using multiprocessing. \n
    :param thread_num: Initial thread num. Default to 3.
    :param url_list: A list consists of url_dict
                    which consists of "url", "content_name", "saving_path".
                    url_list = [
                        {"url": "url_1", "saving_path": "./data/1.jpg"},
                        {"url": "url_2", "saving_path": "./data/2.jpg"},
                        ...
                    ]

    :param headers: requests headers.
    :return:
    """
    thread_num = thread_num if thread_num > 0 else 3
    my_pool = Pool(thread_num)
    for url_dict in url_list:
        my_pool.apply_async(func=img_dl_step, args=(url_dict, headers), callback=saver)

    print("------start------")
    my_pool.close()
    my_pool.join()
    print("------end-------")


if __name__ == "__main__":
    # for testing purpose.
    target_urls = [
        {"url": "url_1", "saving_path": "./data/1.jpg"},
        {"url": "url_2", "saving_path": "./data/2.jpg"},
        {"url": "url_3", "saving_path": "./data/3.jpg"},
        {"url": "url_4", "saving_path": "./data/4.jpg"},
        {"url": "url_5", "saving_path": "./data/5.jpg"},
        {"url": "url_6", "saving_path": "./data/6.jpg"},
        {"url": "url_7", "saving_path": "./data/7.jpg"},
        {"url": "url_8", "saving_path": "./data/8.jpg"},
        {"url": "url_9", "saving_path": "./data/9.jpg"},
        {"url": "url_10", "saving_path": "./data/10.jpg"},
        {"url": "url_11", "saving_path": "./data/11.jpg"},
        {"url": "url_12", "saving_path": "./data/12.jpg"},
    ]
    img_dl(3, target_urls, {"headers": "I am headers. "})
