from __future__ import annotations

from pathlib import Path

from . import downloader, filter_repo, utils


def run(
    repo_list_file: Path | str = "example-files/repo-list.txt",
    blacklist: Path | str | None = "example-files/globblacklist.txt",
    source_code_dir: Path = Path("./temp"),
    ssh_key_path: Path | None = None,
):
    utils.ensure_dir(source_code_dir)
    downloader.download_repos(repo_list_file, source_code_dir, ssh_key_path)
    if blacklist:
        filter_repo.filter_paths(blacklist, source_code_dir)
