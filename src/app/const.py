from enum import Enum

DEFUALT_PASSWORD = "1234"


class FileType(Enum):
    """File types"""

    VIDEO = 1
    IMAGE = 2
    AUDIO = 3
    DOCUMENT = 4


allowed_extensions = {
    1: ['.mp4', '.mov', '.wmv', '.avi', '.mkv', '.webm'],
    2: ['.gift', '.jpeg', '.png', '.svg'],
    3: ['.mp3', '.wav'],
    4:  ['.pdf', '.txt', '.docx', '.pptx']
}
