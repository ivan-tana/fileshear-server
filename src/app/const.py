from enum import Enum


DEFUALT_PASSWORD = "1234"


class FileType(Enum):
    """File types"""

    VIDEO = 1
    IMAGE = 2
    AUDIO = 3
    DOCUMENT = 4
