# github-repo-downloader

Download Github repositories with python.

## Installation

`pip install git+https://github.com/TeiaLabs/github-repo-downloader.git@master`

And on your `requirements.txt`:

`github-repo-downloader @ git+https://github.com/TeiaLabs/github-repo-downloader.git@master`

## Usage

```python
from pathlib import Path

import github_repo_zip_downloader

github_repo_zip_downloader.run(repos_dir=Path("/tmp/"))
```

## CLI usage (WIP)

```bash
github-repo-downloader
```

## Private repos

To use this tool with private repos, make sure your SSH agent has a key with access to them or provide its path to the `custom_ssh_key` kwarg.
