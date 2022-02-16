from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from .loggers import MyLogger

logger = MyLogger.get_logger(__name__)


def ensure_dir(dir_path: Path):
    if dir_path.is_file():
        dir_path = dir_path.parent
    dir_path.mkdir(parents=True, exist_ok=True)


def get_env_var(envvar: str) -> str:
    var = os.getenv(envvar)
    if var is None:
        raise ValueError(f"Environment variable {envvar} unset.")
    return var


def is_non_empty_dir(directory: Path | str, hidden_ok: bool = False) -> bool:
    """
    Return True if the directory exists and contains item(s) else False.

    if not hidden_ok: consider folders with only hidden files as empty.
    """
    expression = r"*" if hidden_ok else r"[!.]*"
    return any(Path(directory).glob(expression))


def read_json(filepath: Path) -> dict[str, str]:
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    logger.debug(f"Loaded {filepath}.")
    return data


def read_multiline_txt(filepath: Path | str) -> list[str]:
    with open(filepath) as f:
        lines = f.read().split("\n")
    if lines[-1] == "":
        lines.pop()
    logger.debug(f"Read {len(lines)} lines from {filepath}.")
    return lines


def save_json(data: dict[str, str], filepath: Path):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    logger.debug(f"Saved {filepath}.")


@contextmanager
def working_directory(newdir: Path | str):
    """
    Change working directory temporarily.

    >>> with working_directory("/tmp"):
    ...     assert os.getcwd() == "/tmp"
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
