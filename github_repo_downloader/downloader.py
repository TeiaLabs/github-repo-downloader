from __future__ import annotations

import os
import re
import shlex
import shutil
import subprocess
from functools import wraps
from pathlib import Path
from typing import Callable

from requests import PreparedRequest
from requests.auth import AuthBase

from . import loggers, metadata, utils

logger = loggers.MyLogger.get_logger(__name__)


class BearerTokenAuth(AuthBase):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


def authenticate(wrapped: Callable) -> Callable:
    # TODO type hints
    @wraps(wrapped)
    def new_func(*args, **kwargs):
        api_token = os.getenv("GITHUB_API_TOKEN")
        if api_token:
            authentication_header = BearerTokenAuth(api_token)
        else:
            authentication_header = None
        return wrapped(*args, api_token=authentication_header, **kwargs)
    return new_func


def parse_url(repo_url: str) -> tuple[str, str] | None:
    """
    Attempt to parse a repo URL into an org and repo name.

    Attempt to parse it as an HTTP URL with a regex.
    If that fails, try to manually parse it as either
    a path in the "org/repo" format or an SSH URL.
    """
    http_url_regex = r"https?://github.com/(?P<org>[\w-]+)/(?P<repo>[\w-]+)"
    if repo_url == "" or repo_url.startswith("#"):
        return None
    match_ = re.match(http_url_regex, repo_url)
    if not match_:
        org, repo = repo_url.split("/")[-2:]
        if org.startswith("git@github.com:"):
            org = org[15:]
        if repo.endswith(".git"):
            repo = repo[:-4]
        return org, repo
    org = match_.group("org")
    repo = match_.group("repo")
    return org, repo


def shallow_clone_repo(
    host: str,
    org_name: str,
    repo_name: str,
    destination_path: Path,
    custom_ssh_key: Path | None,
):
    clone_url = f"{host}:/{org_name}/{repo_name}.git"
    output_path = destination_path / org_name / repo_name
    cmd = f"git clone --depth 1 {clone_url} {output_path}"
    if custom_ssh_key is not None and custom_ssh_key.is_file():
        cmd += f" --config core.sshCommand='ssh -i {custom_ssh_key}'"
    try:
        subprocess.run(shlex.split(cmd), check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Could not clone {org_name}/{repo_name} because of {e}.")
        return
    logger.debug(f"Cloned {org_name}/{repo_name} to {output_path}.")


class RepoCleaner:
    """Delete files not in the supported extensions of a given language."""
    supported_files = {
        "javascript": ["es", "es6", "js", "jsx", "ts", "tsx"],
    }
    cmd = "find {path} -type f ! -regex '{allowed_extensions}' -delete"
    @classmethod
    def run(
        cls,
        org_name: str,
        repo_name: str,
        destination_dir: Path,
        language: str = "javascript",
    ):
        repo_path = destination_dir / org_name / repo_name
        or_regex = r"\|".join(cls.supported_files[language])
        all_files_ending_in = rf".*\.\({or_regex}\)"
        cmd = cls.cmd.format(
            path=repo_path, allowed_extensions=all_files_ending_in
        )
        subprocess.run(shlex.split(cmd), check=False)
        cmd = f"rm -rf {repo_path / '.git'}"
        subprocess.run(shlex.split(cmd), check=False)
        logger.debug(f"Cleaned {org_name}/{repo_name}.")


def download_repos(
    repos_file: Path | str, destination_dir: Path, custom_ssh_key: Path | None
):
    repo_urls = utils.read_multiline_txt(repos_file)
    parsed_urls = list(map(parse_url, repo_urls))
    org_repo_tuples = set(filter(None, parsed_urls))
    host = "git@github.com"
    for org_name, repo_name in org_repo_tuples:
        shallow_clone_repo(
            host, org_name, repo_name, destination_dir, custom_ssh_key
        )
        repo_dir = destination_dir / org_name / repo_name
        if utils.is_non_empty_dir(repo_dir):
            metadata.MetadataExtractor.run(repo_dir)
            RepoCleaner.run(org_name, repo_name, destination_dir)
        else:
            logger.info("Deleting empty repo: %s/%s", org_name, repo_name)
            shutil.rmtree(repo_dir, ignore_errors=True)
