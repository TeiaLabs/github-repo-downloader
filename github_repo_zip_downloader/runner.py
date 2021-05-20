from pathlib import Path

from .downloader import download_repos
from .filter_repo import filter_paths


def main():
    repo_list_file = Path("repo-list.txt")
    blacklist = Path("globfilter.txt")
    repos_dir = Path("./tempo")
    download_repos(repo_list_file, repos_dir)
    filter_paths(blacklist, repos_dir)