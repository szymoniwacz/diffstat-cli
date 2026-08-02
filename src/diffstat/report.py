"""Text and JSON reporters with stable ordering."""

from __future__ import annotations

import json
from typing import Any

from diffstat.analysis import AnalysisResult, path_breakdown
from diffstat.risk import RiskAssessment, rank_files


def build_report_dict(
    result: AnalysisResult,
    risk: RiskAssessment,
    *,
    mode: str,
    repo: str,
    base: str | None,
    head: str | None,
) -> dict[str, Any]:
    ranked = rank_files(result.files)
    return {
        "schema_version": 1,
        "tool": "diffstat",
        "mode": mode,
        "repo": repo,
        "range": {"base": base, "head": head},
        "totals": {
            "files_changed": result.files_changed,
            "lines_added": result.lines_added,
            "lines_deleted": result.lines_deleted,
            "total_churn": result.total_churn,
        },
        "languages": [
            {
                "language": lang,
                "files": files,
                "added": added,
                "deleted": deleted,
                "churn": added + deleted,
            }
            for lang, files, added, deleted in path_breakdown(result.files)
        ],
        "files": [
            {
                "path": f.path,
                "added": f.added,
                "deleted": f.deleted,
                "churn": f.churn,
                "sensitive": f.path in set(risk.sensitive_files),
            }
            for f in ranked
        ],
        "hotspots": [
            {
                "path": f.path,
                "added": f.added,
                "deleted": f.deleted,
                "churn": f.churn,
            }
            for f in result.hotspots
        ],
        "review_risk": {
            "score": risk.score,
            "level": risk.level,
            "reasons": risk.reasons,
            "sensitive_files": risk.sensitive_files,
        },
    }


def format_text(report: dict[str, Any]) -> str:
    totals = report["totals"]
    risk = report["review_risk"]
    lines = [
        "diffstat report",
        f"mode: {report['mode']}",
        f"repo: {report['repo']}",
    ]
    base = report["range"]["base"]
    head = report["range"]["head"]
    if base is not None and head is not None:
        lines.append(f"range: {base}..{head}")
    else:
        lines.append("range: working-tree (vs HEAD)")
    lines.extend(
        [
            "",
            "totals:",
            f"  files_changed: {totals['files_changed']}",
            f"  lines_added: {totals['lines_added']}",
            f"  lines_deleted: {totals['lines_deleted']}",
            f"  total_churn: {totals['total_churn']}",
            "",
            f"review_risk: {risk['level']} ({risk['score']}/100)",
        ]
    )
    for reason in risk["reasons"]:
        lines.append(f"  - {reason}")
    if risk["sensitive_files"]:
        lines.append("sensitive_files:")
        for path in risk["sensitive_files"]:
            lines.append(f"  - {path}")

    lines.append("")
    lines.append("languages:")
    if report["languages"]:
        for lang in report["languages"]:
            lines.append(
                f"  {lang['language']}: files={lang['files']} "
                f"+{lang['added']}/-{lang['deleted']} churn={lang['churn']}"
            )
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("hotspots:")
    if report["hotspots"]:
        for f in report["hotspots"]:
            lines.append(
                f"  {f['path']}: +{f['added']}/-{f['deleted']} churn={f['churn']}"
            )
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("files:")
    if report["files"]:
        for f in report["files"]:
            marker = " [sensitive]" if f["sensitive"] else ""
            lines.append(
                f"  {f['path']}: +{f['added']}/-{f['deleted']} "
                f"churn={f['churn']}{marker}"
            )
    else:
        lines.append("  (none)")

    return "\n".join(lines) + "\n"


def format_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"
