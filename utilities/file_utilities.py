"""
Set of file utility functions
"""

import json


def load_json_from_file(file_path):
    """
    load_json_from_file
    :param file_path:
    :return:
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
