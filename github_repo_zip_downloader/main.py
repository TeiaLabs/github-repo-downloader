import os
import requests
import zipfile
from io import BytesIO
from typing import Optional, Union

from requests import PreparedRequest
from requests.auth import AuthBase


BASE_URL = "https://api.github.com/repos/{}/{}/zipball/{}"


def get_env_var(envvar: str) -> str:
    var = os.getenv(envvar)
    if var is None:
        raise ValueError(f"Environment variable {envvar} unset.")
    return var


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
    api_token: Optional[Union[bool, str]] = None,
    branch: str = "master",
    destination_path: str = ".",
):
    if isinstance(api_token, str):
        authentication_header = BearerTokenAuth(api_token)
    elif api_token:
        authentication_header = BearerTokenAuth(get_env_var("API_TOKEN"))
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


if __name__ == "__main__":
    download_repo("TeiaLabs", "github-repo-zip-downloader")
    download_repo(
        "TeiaLabs", "teia-code-search", True
    )
