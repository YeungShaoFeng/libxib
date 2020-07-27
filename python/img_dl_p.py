from multiprocessing import Pool
from cfg import UNKNOWN_ERROR, TIMED_OUT

try:
    from python.make_dir import make_dir
    from python.get_this_url import get_this_url
    from python.pic_format import pic_format
except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    from make_dir import make_dir
    from get_this_url import get_this_url
    from pic_format import pic_format


class ImageDl:
    def __init__(self, url_list: list, headers: dict, worker_size=3, dynamic_adjust_worker_size=False):
        """
        A downloader for img using multiprocessing. \n
        :param worker_size: Initial thread num. Default to 3.
        :param url_list: A list consists of url_dict
                        which consists of "url", "content_name", "saving_path".
                        url_list = [
                            {"url": "url_1", "saving_path": "./data/1.jpg"},
                            {"url": "url_2", "saving_path": "./data/2.jpg"},
                            ...
                        ]
        :param headers: requests headers.
        :param dynamic_adjust_worker_size: Adjust worker size dynamically if set to True.
        """
        self.url_list = url_list
        self.headers = headers
        self.worker_size = worker_size if worker_size > 0 else 3
        self.MAX_WORKER_SIZE = 10
        self.adjust_worker_size() if dynamic_adjust_worker_size else True

    def saver(self, msg: dict):
        # print("----callback func --pid=%d" % os.getpid())
        content, url = msg["content"], msg["url"]
        if content != UNKNOWN_ERROR:
            # jpg or png.
            content_format = pic_format(content[:8])

            saving_path = f'{msg["saving_path"]}{content_format}'
            content_name = '/'.join(saving_path.split("/")[-2:])

            print(f"Saving '{content_name}' to '{saving_path}'...", end='')
            parent_dir = '/'.join(saving_path.split('/')[:-1])
            make_dir(parent_dir)
            with open(saving_path, "wb") as fp:
                fp.write(content)
            print(" Done. ")
        elif content == TIMED_OUT:
            print(f"\"{url}\" failed due to {TIMED_OUT}. ")
        elif content == UNKNOWN_ERROR:
            print(f"\"{url}\" failed due to {UNKNOWN_ERROR}. ")

    def get(self, url, headers):
        print(f"Getting '{url}' with '{headers}'... ", end='')
        print("Done")
        return url

    def worker(self, url_dict: dict, headers: dict) -> dict:
        """
        A step of img_dl. \n
        :param url_dict: A dict consists of "content_name", "saving_path".
        :param headers: requests headers.
        :return: Downloaded content.
        """
        # test
        # print("pid: {}, ppid: {}".format(os.getpid(), os.getppid()))
        # content = self.get(url_dict["url"], headers)
        # test to print the global variables in the Pool.
        # print(a, end='')
        url = url_dict["url"]
        content = get_this_url(url, headers, text_mode=False)
        return {"content": content, "saving_path": url_dict["saving_path"], "url": url}

    def adjust_worker_size(self):
        worker_size = len(self.url_list) // 10
        self.worker_size = worker_size + 1 if worker_size % 10 else worker_size
        self.worker_size = self.worker_size if self.worker_size < self.MAX_WORKER_SIZE else self.MAX_WORKER_SIZE

    def set_max_worker_size(self, size):
        self.MAX_WORKER_SIZE = size

    def run(self):
        print(f"worker_size: {self.worker_size}")
        my_pool = Pool(self.worker_size)
        for url_dict in self.url_list:
            args = (url_dict, self.headers)
            my_pool.apply_async(func=self.worker, args=args, callback=self.saver)

        print("=== start downloading ===")
        my_pool.close()
        my_pool.join()
        print("=== end downloading ===")


if __name__ == "__main__":
    # for testing purpose.
    target_urls = [
        {"url": "url_1", "saving_path": "./data/1.jpg"},
        {"url": "url_2", "saving_path": "./data/2.jpg"},
        {"url": "url_3", "saving_path": "./data/3.jpg"},
    ]
    img_dl = ImageDl(target_urls, {"headers": "I am headers. "})
    img_dl.run()
