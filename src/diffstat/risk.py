"""Deterministic review-risk heuristics for diffstat-cli."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from diffstat.analysis import AnalysisResult, FileChurn

# Documented MVP sensitive-path substrings / suffixes (case-insensitive).
SENSITIVE_SUBSTRINGS = (
    ".env",
    "id_rsa",
    "credentials",
    "secret",
    "passwd",
    "password",
    "/auth/",
    "token",
    "private_key",
)
SENSITIVE_SUFFIXES = (
    ".pem",
    ".key",
    ".p12",
    ".pfx",
)


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    reasons: list[str]
    sensitive_files: list[str]


def is_sensitive_path(path: str) -> bool:
    lowered = path.lower().replace("\\", "/")
    name = PurePosixPath(lowered).name
    if any(s in lowered for s in SENSITIVE_SUBSTRINGS):
        return True
    return any(name.endswith(suf) for suf in SENSITIVE_SUFFIXES)


def assess_risk(result: AnalysisResult) -> RiskAssessment:
    """Score review risk from churn, file count, and sensitive paths.

    Score is 0–100. Level bands: low (0–24), medium (25–59), high (60–100).
    """
    score = 0
    reasons: list[str] = []

    # Churn contribution (max 40).
    churn = result.total_churn
    if churn >= 1000:
        score += 40
        reasons.append(f"very high churn ({churn} lines)")
    elif churn >= 400:
        score += 30
        reasons.append(f"high churn ({churn} lines)")
    elif churn >= 100:
        score += 20
        reasons.append(f"moderate churn ({churn} lines)")
    elif churn > 0:
        score += 10
        reasons.append(f"low churn ({churn} lines)")

    # File-count contribution (max 30).
    files = result.files_changed
    if files >= 40:
        score += 30
        reasons.append(f"many files changed ({files})")
    elif files >= 15:
        score += 20
        reasons.append(f"elevated file count ({files})")
    elif files >= 5:
        score += 10
        reasons.append(f"several files changed ({files})")

    sensitive = sorted(f.path for f in result.files if is_sensitive_path(f.path))
    if sensitive:
        # Sensitive paths contribution (max 30).
        bump = min(30, 15 + 5 * (len(sensitive) - 1))
        score += bump
        reasons.append(f"{len(sensitive)} sensitive-path file(s)")

    score = min(100, score)
    if score >= 60:
        level = "high"
    elif score >= 25:
        level = "medium"
    else:
        level = "low"

    if not reasons:
        reasons.append("no material churn")

    return RiskAssessment(
        score=score,
        level=level,
        reasons=reasons,
        sensitive_files=sensitive,
    )


def rank_files(files: list[FileChurn]) -> list[FileChurn]:
    """Rank files for review: sensitive first, then by churn, then path."""
    return sorted(
        files,
        key=lambda f: (0 if is_sensitive_path(f.path) else 1, -f.churn, f.path),
    )
