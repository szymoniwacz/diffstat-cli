"""Aggregate churn and hotspot statistics from git numstat rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from diffstat.gitutil import NumstatRow


@dataclass(frozen=True)
class FileChurn:
    path: str
    added: int
    deleted: int

    @property
    def churn(self) -> int:
        return self.added + self.deleted


@dataclass(frozen=True)
class AnalysisResult:
    files: list[FileChurn]
    files_changed: int
    lines_added: int
    lines_deleted: int
    total_churn: int
    hotspots: list[FileChurn]


def language_bucket(path: str) -> str:
    suffix = PurePosixPath(path).suffix.lower()
    if not suffix:
        return "other"
    return suffix.lstrip(".")


def analyze(rows: list[NumstatRow], *, hotspot_limit: int = 10) -> AnalysisResult:
    files = sorted(
        (FileChurn(path=r.path, added=r.added, deleted=r.deleted) for r in rows),
        key=lambda f: (-f.churn, f.path),
    )
    lines_added = sum(f.added for f in files)
    lines_deleted = sum(f.deleted for f in files)
    hotspots = files[:hotspot_limit]
    return AnalysisResult(
        files=files,
        files_changed=len(files),
        lines_added=lines_added,
        lines_deleted=lines_deleted,
        total_churn=lines_added + lines_deleted,
        hotspots=hotspots,
    )


def path_breakdown(files: list[FileChurn]) -> list[tuple[str, int, int, int]]:
    """Return (language, files, added, deleted) sorted by churn then name."""
    buckets: dict[str, list[int]] = {}
    for f in files:
        key = language_bucket(f.path)
        stats = buckets.setdefault(key, [0, 0, 0])
        stats[0] += 1
        stats[1] += f.added
        stats[2] += f.deleted
    items = [
        (lang, counts[0], counts[1], counts[2]) for lang, counts in buckets.items()
    ]
    return sorted(items, key=lambda t: (-(t[2] + t[3]), t[0]))
