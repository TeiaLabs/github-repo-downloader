from __future__ import annotations

import re
import zipfile
from io import BytesIO
from pathlib import Path

import requests
from requests import PreparedRequest
from requests.auth import AuthBase

from . import utils

BASE_URL = "https://api.github.com/repos/{}/{}/zipball/{}"
GITHUB_URL_REGEX =  r"https?://github.com/(?P<org>[\w-]+)/(?P<repo>[\w-]+)"


class BearerTokenAuth(AuthBase):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


def download_repo(
    org_name: str,
    repo_name: str,
    api_token: bool | str | None = None,
    branch: str | None = "master",
    destination_path: Path | str = ".",
):
    if isinstance(api_token, str):
        authentication_header = BearerTokenAuth(api_token)
    elif api_token:
        authentication_header = BearerTokenAuth(utils.get_env_var("API_TOKEN"))
    elif api_token is None:
        authentication_header = None
    else:
        raise ValueError("Param 'api_token' got unexpected value.")

    zip_url = BASE_URL.format(org_name, repo_name, branch)
    res = requests.get(
        zip_url,
        headers={"Accept": "application/vnd.github.v3.raw"},
        auth=authentication_header,
        timeout=90,
        allow_redirects=True,
        stream=True,
    )
    z = zipfile.ZipFile(BytesIO(res.content))
    z.extractall(path=destination_path)


def parse_url(repo_url: str) -> tuple[str, str]:
    match_ = re.match(GITHUB_URL_REGEX, repo_url)
    if not match_:
        raise ValueError("Invalid URL:", repo_url)
    org = match_.group("org")
    repo = match_.group("repo")
    return org, repo


def download_repos(repos_file: Path, destination_dir: Path | str):
    repos = utils.read_multiline_txt(repos_file)
    for repo_url in repos:
        try:
            org, repo = parse_url(repo_url)
        except ValueError as e:
            print(e)
            continue
        download_repo(
            org, repo, True, destination_path=destination_dir
        )


if __name__ == "__main__":
    download_repo("TeiaLabs", "github-repo-zip-downloader")
    download_repo(
        "TeiaLabs", "codesearch-teia-set", True
    )
