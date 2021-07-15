# github-repo-zip-downloader

Download Github repositories with python.

## Installation

`pip install git+https://github.com/TeiaLabs/github-repo-zip-downloader.git@master`

And on your `requirements.txt`:

`github-repo-zip-downloader @ git+https://github.com/TeiaLabs/github-repo-zip-downloader.git@master`

## Usage

```python
from pathlib import Path

import github_repo_zip_downloader

github_repo_zip_downloader.run(repos_dir=Path("/tmp/"))
```

## Low level usage

```python
from github_repo_zip_downloader import download_repo

download_repo("TeiaLabs", "github-repo-zip-downloader")
```

## Private repos

To use this tool with private repos, create a Github API token for yourself at <https://github.com/settings/tokens/new>.

Then export it in your env with `export API_TOKEN=ghp_...`.
