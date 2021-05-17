# github-repo-zip-downloader

Download Github repositories with python.

```python
from github_repo_zip_downloader import download_repo

download_repo("TeiaLabs", "github-repo-zip-downloader")
```

If you're into private repos, you can also use this tool.
Just don't forget to create a Github API token for yourself at <https://github.com/settings/tokens/new>.

The recommended way to use it is to export it in your env with `export API_TOKEN=ghp_...` and `download_repo("org", "repo", api_token=True)`.

But you could also pass the token string as an argument directly.
