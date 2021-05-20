from __future__ import annotations

import os
from pathlib import Path


def get_env_var(envvar: str) -> str:
    var = os.getenv(envvar)
    if var is None:
        raise ValueError(f"Environment variable {envvar} unset.")
    return var


def read_multiline_txt(filepath: Path | str) -> list[str]:
    with open(filepath) as f:
        lines = f.read().split("\n")
    if lines[-1] == "":
        lines.pop()
    return lines
