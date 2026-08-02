"""Tests for diffstat-cli bootstrap scaffold."""

from diffstat import __version__
from diffstat.cli import build_parser, main


def test_version():
    assert __version__ == "0.1.0"


def test_parser_has_version():
    parser = build_parser()
    actions = [a.dest for a in parser._actions]
    assert "version" in actions


def test_main_help_exits_zero():
    try:
        code = main(["--help"])
    except SystemExit as exc:
        code = exc.code
    assert code == 0
