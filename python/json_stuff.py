from os import mkdir as os_mkdir
from os.path import exists as os_path_exists
from json import dump as json_dump

def save_data_to_json_file(data, jsonFilePath, indentation=None):
    os_mkdir(jsonFilePath) if (not os_path_exists(jsonFilePath)) else True
    if (indentation):
        print("\n{}".format(indentation))
    print("Saving data to '{}'... ".format(indentation, jsonFilePath), end="")
    with open(jsonFilePath, "w", encoding="utf-8") as f:
        json_dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)
    print("Done. \n")
