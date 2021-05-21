from __future__ import annotations

from pathlib import Path

from . import downloader, filter_repo, utils


def run(
    repo_list_file: Path | str = "repo-list.txt",
    blacklist: Path | str | None = "globblacklist.txt",
    repos_dir: Path = Path("./temp"),
):
    utils.ensure_dir(repos_dir)
    downloader.download_repos(repo_list_file, repos_dir)
    if blacklist:
        filter_repo.filter_paths(blacklist, repos_dir)
