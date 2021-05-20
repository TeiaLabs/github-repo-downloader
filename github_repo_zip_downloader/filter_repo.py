import shutil
from pathlib import Path

from . import utils


def delete_matches(patterns: list[str], dir_path: Path):
    for pattern in patterns:
        matches = dir_path.glob(rf"*/{pattern}")
        for file in matches:
            if file.is_dir():
                shutil.rmtree(file)
            else:
                file.unlink()


def filter_paths(patterns_file: Path, dir_path: Path):
    patterns = utils.read_multiline_txt(patterns_file)
    delete_matches(patterns, dir_path)
