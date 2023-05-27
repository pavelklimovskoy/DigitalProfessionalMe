# -*- coding: utf-8 -*-

"""
    Служебные модули для поддержания работы сервера

    28.05.2023
"""

import sys


def check_python_version() -> None:
    """
    Функция для проверки версии интерпретатора Python
    :return:
    """
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro

    if micro < 3 or minor < 10:
        raise Exception("Неверная версия Python, необходима версия старше 3.10")