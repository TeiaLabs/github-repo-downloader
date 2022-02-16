from __future__ import annotations

import itertools
import shutil
from pathlib import Path

from . import loggers, utils

logger = loggers.MyLogger.get_logger(__name__)


def delete_matches(patterns: list[str], dir_path: Path):
    matches_list = [dir_path.glob(rf"*/{pattern}") for pattern in patterns]
    matches = set(itertools.chain(*matches_list))
    for file in matches:
        if file.is_dir():
            shutil.rmtree(file)
        else:
            try:
                file.unlink()
            except FileNotFoundError:
                # file might've already been deleted by an rmtree()
                pass
    logger.debug(f"Deleted {len(matches)} matches.")


def filter_paths(patterns_file: Path | str, dir_path: Path):
    patterns = utils.read_multiline_txt(patterns_file)
    delete_matches(patterns, dir_path)
