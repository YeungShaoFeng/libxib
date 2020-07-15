from os import makedirs as os_makedirs


def make_dir(dir_path: str) -> None:
    """
    make the directories recursively. \n
    :param dir_path: The path to that directory.
    :return: True on success. | False on failure.
    """
    try:
        os_makedirs(dir_path)
    except FileExistsError:
        print(dir_path + " exists. ")
