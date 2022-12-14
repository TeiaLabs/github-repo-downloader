import dotenv
import os
from typing import Literal

from github import Github
from tap import Tap

dotenv.load_dotenv()


class Args(Tap):
    org: str  # Github Organization
    output: Literal["http", "ssh", "default"] = "default"  # Choose URL protocol.


def list_repos(github, org):
    for repo in github.get_organization(org).get_repos():
        print(f"{args.org}/{repo.name}")

def list_repos_http(github, org):
    for repo in github.get_organization(org).get_repos():
        print(f"https://github.com/{org}/{repo.name}")


def list_repos_ssh(github, org):
     for repo in github.get_organization(org).get_repos():
        print(f"git@github.com:{args.org}/{repo.name}")


def main(github_client: Github, org_name: str):
    if args.output == "ssh":
        list_repos_ssh(github_client, org_name)
    elif args.output == "http":
        list_repos_http(github_client, org_name)
    elif args.output == "default":
        list_repos(github_client, org_name)


if __name__ == "__main__":
    g = Github(os.getenv("GITHUB_ACESS_TOKEN"))
    args = Args(underscores_to_dashes=True).parse_args()
    main(g, args.org)
