"""Local git adapter for diffstat-cli."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


class GitError(Exception):
    """Raised when a local git operation fails in a user-visible way."""

    def __init__(self, message: str, *, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class NumstatRow:
    path: str
    added: int
    deleted: int


def _run_git(repo: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GitError("git is not available on PATH", exit_code=2) from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise GitError(detail or "git command failed", exit_code=3)
    return completed.stdout


def resolve_repo(path: Path) -> Path:
    repo = path.expanduser().resolve()
    if not repo.exists():
        raise GitError(f"path does not exist: {repo}", exit_code=2)
    if not repo.is_dir():
        raise GitError(f"path is not a directory: {repo}", exit_code=2)
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GitError("git is not available on PATH", exit_code=2) from exc
    if completed.returncode != 0:
        raise GitError(f"not a git repository: {repo}", exit_code=2)
    return Path(completed.stdout.strip())


def collect_numstat(
    repo: Path,
    *,
    base: str | None = None,
    head: str | None = None,
) -> list[NumstatRow]:
    """Return numstat rows for working tree vs HEAD, or for base..head."""
    if (base is None) != (head is None):
        raise GitError(
            "both --base and --head are required when specifying a range",
            exit_code=2,
        )

    if base is None and head is None:
        # Working tree (staged + unstaged) compared to HEAD.
        stdout = _run_git(repo, ["diff", "--numstat", "HEAD"])
    else:
        assert base is not None and head is not None
        # Validate refs before asking for numstat so errors are clearer.
        _run_git(repo, ["rev-parse", "--verify", f"{base}^{{commit}}"])
        _run_git(repo, ["rev-parse", "--verify", f"{head}^{{commit}}"])
        stdout = _run_git(repo, ["diff", "--numstat", base, head])

    rows: list[NumstatRow] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_s, deleted_s, path = parts[0], parts[1], parts[2]
        # Binary files report "-" for added/deleted.
        added = 0 if added_s == "-" else int(added_s)
        deleted = 0 if deleted_s == "-" else int(deleted_s)
        rows.append(NumstatRow(path=path, added=added, deleted=deleted))
    return rows
