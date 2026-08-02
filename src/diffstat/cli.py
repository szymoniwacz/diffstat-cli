"""Command-line interface for diffstat-cli."""

from __future__ import annotations

import argparse
import sys

from diffstat import __version__


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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    if argv is None:
        argv_list = sys.argv[1:]
    else:
        argv_list = list(argv)
    if not argv_list:
        parser.print_help()
        return 0
    parser.parse_args(argv_list)
    return 0


if __name__ == "__main__":
    sys.exit(main())
