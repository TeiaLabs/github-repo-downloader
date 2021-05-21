import logging
import sys
from pathlib import Path

from . import utils

LOG_FILE_PATH = Path("./logs/github-repo-zip-downloader.log")
utils.ensure_dir(LOG_FILE_PATH)
FILE_HANDLER = logging.FileHandler(filename=LOG_FILE_PATH)
LOG_FILE_MESSAGE_FORMAT = logging.Formatter(" ".join((
    "[%(asctime)s]",
    "%(levelname)s -",
    "%(message)s",
)))
FILE_HANDLER.setFormatter(LOG_FILE_MESSAGE_FORMAT)
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
LOG_STREAM_MESSAGE_FORMAT = logging.Formatter("%(message)s")
STDOUT_HANDLER.setFormatter(LOG_STREAM_MESSAGE_FORMAT)

TO_FILE = True
TO_STDOUT = True


def get_logger():
    handlers = []
    if TO_FILE:
        handlers.append(FILE_HANDLER)
    if TO_STDOUT:
        handlers.append(STDOUT_HANDLER)
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
    )
    return logging.getLogger()
