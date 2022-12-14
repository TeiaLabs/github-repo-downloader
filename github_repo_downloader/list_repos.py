import dotenv
import os
from typing import Literal

from tap import Tap
from github import Github

class Args(Tap):
    org: str  # Github Organization
    output: Literal["http", "ssh", "default"] = "default"  # Choose URL protocol.
#functional progarming it so i dosent use global variables:
args = Args(underscores_to_dashes=True).parse_args()


dotenv.load_dotenv()
g = Github(os.getenv("GITHUB_ACESS_TOKEN"))


def lis_repos(github, org):
    for repo in github.get_organization(org).get_repos():
        print(f"{args.org}/{repo.name}")

def list_repos_http(github, org):
    for repo in github.get_organization(org).get_repos():
        print(f"https://github.com/{org}/{repo.name}")


def list_repos_ssh(github, org):
     for repo in github.get_organization(org).get_repos():
        print(f"git@github.com:{args.org}/{repo.name}")

if __name__ == "__main__":
    if args.output == "ssh":
        list_repos_ssh(g, args.org)
    elif args.output == "http":
        list_repos_http(g, args.org)
    elif args.output == "default":
        lis_repos(g, args.org)