"""Command-line interface for diffstat-cli."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from diffstat import __version__
from diffstat.analysis import analyze
from diffstat.gitutil import GitError, collect_numstat, resolve_repo
from diffstat.report import build_report_dict, format_json, format_text
from diffstat.risk import assess_risk

EXIT_OK = 0
EXIT_EMPTY = 1
EXIT_USAGE = 2
EXIT_GIT = 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="diffstat",
        description="Local-first git diff churn and review-risk signals.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"diffstat {__version__}",
    )
    sub = parser.add_subparsers(dest="command")

    analyze_p = sub.add_parser(
        "analyze",
        help="Analyze a local git working tree or commit range",
    )
    analyze_p.add_argument(
        "--path",
        default=".",
        help="Path to a local git repository (default: current directory)",
    )
    analyze_p.add_argument(
        "--base",
        default=None,
        help="Range base ref (requires --head)",
    )
    analyze_p.add_argument(
        "--head",
        default=None,
        help="Range head ref (requires --base)",
    )
    analyze_p.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON on stdout",
    )
    analyze_p.add_argument(
        "--hotspot-limit",
        type=int,
        default=10,
        help="Max hotspot rows in the report (default: 10)",
    )
    return parser


def _run_analyze(args: argparse.Namespace) -> int:
    if (args.base is None) != (args.head is None):
        print(
            "error: both --base and --head are required for a commit range",
            file=sys.stderr,
        )
        return EXIT_USAGE
    if args.hotspot_limit < 1:
        print("error: --hotspot-limit must be >= 1", file=sys.stderr)
        return EXIT_USAGE

    try:
        repo = resolve_repo(Path(args.path))
        rows = collect_numstat(repo, base=args.base, head=args.head)
    except GitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.exit_code

    result = analyze(rows, hotspot_limit=args.hotspot_limit)
    if result.files_changed == 0:
        print("error: empty diff (no file changes)", file=sys.stderr)
        return EXIT_EMPTY

    risk = assess_risk(result)
    mode = "range" if args.base is not None else "working-tree"
    report = build_report_dict(
        result,
        risk,
        mode=mode,
        repo=str(repo),
        base=args.base,
        head=args.head,
    )
    output = format_json(report) if args.json else format_text(report)
    sys.stdout.write(output)
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    if argv is None:
        argv_list = sys.argv[1:]
    else:
        argv_list = list(argv)
    if not argv_list:
        parser.print_help()
        return EXIT_OK
    args = parser.parse_args(argv_list)
    if args.command is None:
        parser.print_help()
        return EXIT_OK
    if args.command == "analyze":
        return _run_analyze(args)
    print(f"error: unknown command: {args.command}", file=sys.stderr)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
