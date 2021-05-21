from __future__ import annotations

from pathlib import Path

from .downloader import download_repos
from .filter_repo import filter_paths


def run(
    repo_list_file: Path | str = "repo-list.txt",
    blacklist: Path | str | None = "globblacklist.txt",
    repos_dir: Path = Path("./temp"),
):
    download_repos(repo_list_file, repos_dir)
    if blacklist:
        filter_paths(blacklist, repos_dir)
