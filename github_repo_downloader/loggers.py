from __future__ import annotations

import logging
import sys
from pathlib import Path


class MyLogger:
    to_file = False
    to_stdout = True

    Path("./logs/").mkdir(exist_ok=True)
    log_file_path = Path("./logs/file.log")
    file_handler = logging.FileHandler(filename=log_file_path)
    log_file_message_format = logging.Formatter(
        " ".join(
            (
                "[%(asctime)s]",
                "'%(name)s'",
                "{%(filename)s:%(lineno)d}",
                "%(levelname)s -",
                "%(message)s",
            )
        )
    )
    file_handler.setFormatter(log_file_message_format)
    stdout_handler = logging.StreamHandler(sys.stdout)
    log_stream_message_format = logging.Formatter("%(levelname)s - %(message)s")
    stdout_handler.setFormatter(log_stream_message_format)

    @classmethod
    def get_logger(cls, name: str | None = None):
        handlers: list[logging.Handler] = []
        if cls.to_file:
            handlers.append(cls.file_handler)
        if cls.to_stdout:
            handlers.append(cls.stdout_handler)
        logger = logging.getLogger(name)
        logger.setLevel(level=logging.INFO)
        for h in handlers:
            logger.addHandler(h)
        # don't propagate to root logger
        logger.propagate = False
        return logger
