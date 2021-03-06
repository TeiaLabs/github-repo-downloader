from __future__ import annotations

import setuptools


def read_multiline_as_list(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8") as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = read_multiline_as_list("requirements.txt")

setuptools.setup(
    name="github-repo-downloader",
    version="2.0.0",
    author="Teialabs",
    author_email="nei@teialabs.com",
    description="Python modules to batch clone Github repositories, extract metadata, and filter out undesirable files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeiaLabs/github-repo-downloader/",
    packages=setuptools.find_packages(),
    # classifiers=classifiers,
    # keywords='web api, restful, AI, NLP, retrieval, neural code search',
    entry_points={
        "console_scripts": [
            "github-repo-downloader=github_repo_downloader.runner:run",
        ],
    },
    python_requires=">=3.8, <3.10",
    install_requires=requirements,
)
