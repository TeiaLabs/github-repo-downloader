from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import TypedDict, cast

from . import loggers, utils

logger = loggers.MyLogger.get_logger(__name__)


class RepoMetadata(TypedDict):
    commit_hash: str
    commit_date: str
    language: str


def run_cmd_on_dir(cmd: str, dir_path: Path) -> str | None:
    splat_cmd = shlex.split(cmd)
    with utils.working_directory(dir_path):
        proc = subprocess.run(splat_cmd, capture_output=True, check=True)
    if proc.stdout:
        return proc.stdout.decode("utf-8").strip()
    return None


class MetadataExtractor:
    commit_date_cmd = r"git show -s --format=%ci HEAD"
    commit_hash_cmd = "git rev-parse --verify HEAD"

    @classmethod
    def get_commit_date(cls, repo_path: Path) -> str:
        timestamp = run_cmd_on_dir(cls.commit_date_cmd, repo_path)
        if not timestamp:
            logger.error(f"Failed to get commit date for {repo_path}.")
            return "1999-12-31 00:00:00 -0300"
        return timestamp

    @classmethod
    def get_commit_hash(cls, repo_path: Path) -> str:
        sha1 = run_cmd_on_dir(cls.commit_hash_cmd, repo_path)
        if not sha1:
            logger.error(f"Failed to get commit hash for {repo_path}.")
            return "master"
        return sha1

    @staticmethod
    def get_language(repo_path: Path) -> str:
        return "javascript"

    @staticmethod
    def read(repo_path: Path) -> RepoMetadata:
        obj = utils.read_json(repo_path.with_suffix(".json"))
        return cast(RepoMetadata, obj)

    @classmethod
    def run(cls, repo_path: Path):
        commit_date = cls.get_commit_date(repo_path)
        commit_hash = cls.get_commit_hash(repo_path)
        language = cls.get_language(repo_path)
        cls.save_metadata(commit_date, commit_hash, language, repo_path)

    @staticmethod
    def save_metadata(
        commit_date: str,
        commit_hash: str,
        language: str,
        repo_path: Path,
    ):
        metadata = {
            "commit_date": commit_date,
            "commit_hash": commit_hash,
            "language": language,
        }
        metadata_path = repo_path.with_suffix(".json")
        utils.save_json(metadata, metadata_path)
        logger.debug(f"Saved metadata to {metadata_path}.")
