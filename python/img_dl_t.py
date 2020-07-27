from threading import Thread
from threading import Lock
from queue import Queue
from time import sleep
from cfg import UNKNOWN_ERROR, TIMED_OUT

try:
    from python.make_dir import make_dir
    from python.get_this_url import get_this_url
    from python.pic_format import pic_format
    from python.Logger import Logger
except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    from make_dir import make_dir
    from get_this_url import get_this_url
    from pic_format import pic_format
    from Logger import Logger

exitFlag = False
queue_lock = Lock()


# """
# TEST
# """
# from make_dir import make_dir
# # from get_this_url import get_this_url
# from pic_format import pic_format
#
# UNKNOWN_ERROR = "unknown-error"
# TIMED_OUT_TIME = 20
# TIMED_OUT = "TIMED_OUT"
#
#
# def get(url, headers):
#     print(f"Getting '{url}' with '{headers}'... ", end='')
#     sleep(0.5)
#     print("Done")
#     return {"content": b"I'm content. ",
#             "url": url,
#             "saving_path": "./data/1"
#             }
# """
# TEST
# """


def saver(msg: dict, text_mod=True):
    """
    A saver. \n
    :param msg: A dict. {"content": ..., "saving_path": ..., "url": ...}
    :param text_mod: "w" if set to True, "wb" if set to False
    :return:
    """
    # print("----callback func --pid=%d" % os.getpid())
    content, url = msg["content"], msg["url"]
    if content == TIMED_OUT:
        Logger.log([saver, f"\"{url}\" failed due to {TIMED_OUT}. "])
    elif content == UNKNOWN_ERROR:
        Logger.log([saver, f"\"{url}\" failed due to {UNKNOWN_ERROR}. "])
    else:
        content_format = pic_format(content[:8])
        saving_path = f'{msg["saving_path"]}.{content_format}'
        content_name = '/'.join(saving_path.split("/")[-2:])
        Logger.log([saver, f"Saving '{content_name}' to '{saving_path}'"])
        make_dir('/'.join(saving_path.split('/')[:-1]))
        if text_mod:
            with open(saving_path, 'w', encoding='utf-8') as fp:
                fp.write(content)
        else:
            with open(saving_path, "wb") as fp:
                fp.write(content)


class DlWorker(Thread):
    """ Download worker using Thread. """

    def __init__(self, worker_id, worker_name, worker_queue, headers):
        """
        :param worker_id: worker id.
        :param worker_name: worker name.
        :param worker_queue: q queue obj consists of working tasks.
        :param headers: requests headers.
        """
        Thread.__init__(self)
        self.id, self.name = worker_id, worker_name
        self.headers, self.queue = headers, worker_queue

    def run(self):
        """
        The worker starts downloading.\n
        :return: None
        """
        while not exitFlag:
            if not self.queue.empty():
                queue_lock.acquire()
                data = self.queue.get()[0]
                queue_lock.release()
                url = data["url"]
                Logger.log([f"[{self.name}] ", f'is getting: "{url}"'])
                data["content"] = get_this_url(data["url"], self.headers, text_mode=False)["content"]
                saver(data, text_mod=False)
                # saver(get(data["url"], self.headers))
            sleep(0.1)


class ImageDl(Thread):
    """ A downloader for img using multiprocessing. """

    def __init__(self, url_list: list, headers: dict, worker_size=3, dynamic_adjust_worker_size=False):
        """
        :param worker_size: Initial thread num. Default to 3.
        :param url_list: A list consists of url_dict
                        which consists of "url", "content_name", "saving_path"(no format).
                        url_list = [
                            {"url": "url_1", "saving_path": "./data/1"},
                            {"url": "url_2", "saving_path": "./data/2"},
                            ...
                        ]
        :param headers: requests headers.
        :param dynamic_adjust_worker_size: Adjust worker size dynamically if set to True.
        """
        Thread.__init__(self)
        self.url_list = url_list
        self.headers = headers
        self.worker_size = worker_size if worker_size > 0 else 3
        self.MAX_WORKER_SIZE = 20
        self.adjust_worker_size() if dynamic_adjust_worker_size else True
        self.work_queue = Queue(len(self.url_list))
        self.worker_group, self.worker_names = [], []
        self.work_per_worker = 5

    def adjust_worker_size(self):
        """
        Adjust worker size by the length of self.url_list. max is 10. \n
        :return: None
        """
        worker_size = len(self.url_list) // self.work_per_worker
        self.worker_size = worker_size + 1 if worker_size % self.work_per_worker else worker_size
        self.worker_size = self.worker_size if self.worker_size < self.MAX_WORKER_SIZE else self.MAX_WORKER_SIZE
        Logger.log(
            [f"[{__class__.__name__}]", self.adjust_worker_size, f"adjusted worker size to: [{self.worker_size}]"]
        )

    def set_max_worker_size(self, size):
        """
        Set the max_worker_size. \n
        :param size: int
        :return: None
        """
        self.MAX_WORKER_SIZE = size
        Logger.log(
            [f"[{__class__.__name__}]", self.set_max_worker_size, f'set max_worker_size to: [{self.MAX_WORKER_SIZE}]']
        )

    def fill_up_self_work_queue(self):
        """
        Fill up self.work_queue which's consists of tasks.
        :return: None
        """
        Logger.log([f"[{__class__.__name__}]", self.fill_up_self_work_queue, 'Start filling up work queue...'])
        queue_lock.acquire()
        [self.work_queue.put((url_dict,)) for url_dict in self.url_list]
        queue_lock.release()
        Logger.log([f"[{__class__.__name__}]", self.fill_up_self_work_queue, 'Done. '])

    def grouping_workers(self):
        worker_names = []
        Logger.log([f"[{__class__.__name__}]", self.grouping_workers, 'Start grouping up workers...'])
        for i in range(self.worker_size):
            worker_names.append(f"Worker-{str(i)}")
            worker = DlWorker(i, worker_names[i], self.work_queue, self.headers)
            worker.start()
            self.worker_group.append(worker)
        Logger.log([f"[{__class__.__name__}]", self.grouping_workers, f'Grouped [{len(self.worker_group)}] workers. '])

    def run(self):
        """
        Grouping workers and starting downloading. \n
        :return: None
        """
        self.fill_up_self_work_queue()
        self.grouping_workers()
        Logger.log([f'[{__class__.__name__}]', self.run, "=== start downloading ==="])
        while not self.work_queue.empty():
            sleep(0.1)
            pass
        sleep(1)
        global exitFlag
        exitFlag = True
        Logger.log([f'[{__class__.__name__}]', self.run, "=== end downloading ==="])
        for worker in self.worker_group:
            worker.join()
        Logger.log([f'[{__class__.__name__}]', self.run, "Workers's joined. "])
        """
        For The Next Run. 
        """
        exitFlag = False


if __name__ == "__main__":
    # for testing purpose.
    target_urls = [
        {"url": "url_1", "saving_path": "./data/1.jpg"},
        {"url": "url_2", "saving_path": "./data/2.jpg"},
        {"url": "url_3", "saving_path": "./data/3.jpg"},
    ]
    img_dl = ImageDl(target_urls, {"headers": "I am headers. "})
    img_dl.run()
    print("Exit main thread. ")
