"""Tests for diffstat analyze command and helpers."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from diffstat.analysis import analyze, language_bucket
from diffstat.cli import main
from diffstat.gitutil import NumstatRow, collect_numstat, resolve_repo
from diffstat.risk import assess_risk, is_sensitive_path


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "initial")
    return repo


def test_language_bucket():
    assert language_bucket("src/a.py") == "py"
    assert language_bucket("Makefile") == "other"


def test_is_sensitive_path():
    assert is_sensitive_path(".env")
    assert is_sensitive_path("certs/server.pem")
    assert is_sensitive_path("app/auth/login.py")
    assert not is_sensitive_path("src/cli.py")


def test_analyze_sorts_by_churn():
    rows = [
        NumstatRow(path="b.txt", added=1, deleted=0),
        NumstatRow(path="a.txt", added=5, deleted=5),
    ]
    result = analyze(rows)
    assert result.files[0].path == "a.txt"
    assert result.total_churn == 11


def test_risk_increases_for_sensitive_and_churn():
    rows = [NumstatRow(path=".env", added=20, deleted=0)]
    result = analyze(rows)
    risk = assess_risk(result)
    assert risk.level in {"medium", "high"}
    assert ".env" in risk.sensitive_files


def test_resolve_repo_rejects_non_git(tmp_path: Path):
    from diffstat.gitutil import GitError

    with pytest.raises(GitError):
        resolve_repo(tmp_path)


def test_working_tree_analyze(git_repo: Path, capsys: pytest.CaptureFixture[str]):
    (git_repo / "app.py").write_text("print('x')\n" * 5, encoding="utf-8")
    _git(git_repo, "add", "app.py")
    code = main(["analyze", "--path", str(git_repo)])
    captured = capsys.readouterr()
    assert code == 0
    assert "files_changed: 1" in captured.out
    assert "app.py" in captured.out
    assert "review_risk:" in captured.out


def test_json_analyze_stable_keys(git_repo: Path, capsys: pytest.CaptureFixture[str]):
    (git_repo / "a.py").write_text("a\n", encoding="utf-8")
    _git(git_repo, "add", "a.py")
    _git(git_repo, "commit", "-m", "add a")
    (git_repo / "b.py").write_text("b\n", encoding="utf-8")
    _git(git_repo, "add", "b.py")
    _git(git_repo, "commit", "-m", "add b")
    code = main(
        [
            "analyze",
            "--path",
            str(git_repo),
            "--base",
            "HEAD~1",
            "--head",
            "HEAD",
            "--json",
        ]
    )
    captured = capsys.readouterr()
    assert code == 0
    payload = json.loads(captured.out)
    assert payload["schema_version"] == 1
    assert payload["totals"]["files_changed"] == 1
    assert payload["files"][0]["path"] == "b.py"
    assert "score" in payload["review_risk"]


def test_empty_diff_exits_nonzero(git_repo: Path, capsys: pytest.CaptureFixture[str]):
    code = main(["analyze", "--path", str(git_repo)])
    captured = capsys.readouterr()
    assert code == 1
    assert "empty diff" in captured.err


def test_non_git_path_exits_nonzero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    code = main(["analyze", "--path", str(tmp_path)])
    captured = capsys.readouterr()
    assert code == 2
    assert "not a git repository" in captured.err


def test_invalid_range_exits_nonzero(
    git_repo: Path, capsys: pytest.CaptureFixture[str]
):
    code = main(
        [
            "analyze",
            "--path",
            str(git_repo),
            "--base",
            "no-such-ref",
            "--head",
            "HEAD",
        ]
    )
    captured = capsys.readouterr()
    assert code == 3
    assert captured.err.startswith("error:")


def test_base_without_head_exits_usage(
    git_repo: Path, capsys: pytest.CaptureFixture[str]
):
    code = main(["analyze", "--path", str(git_repo), "--base", "HEAD"])
    captured = capsys.readouterr()
    assert code == 2
    assert "both --base and --head" in captured.err


def test_collect_numstat_range(git_repo: Path):
    (git_repo / "x.txt").write_text("one\n", encoding="utf-8")
    _git(git_repo, "add", "x.txt")
    _git(git_repo, "commit", "-m", "add x")
    rows = collect_numstat(git_repo, base="HEAD~1", head="HEAD")
    assert len(rows) == 1
    assert rows[0].path == "x.txt"
