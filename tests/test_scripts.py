"""Unit tests for json_sort.scripts (CLI)."""
from unittest.mock import patch

import pytest

from json_sort.scripts import CommonParser, fromlocal, fromurl


class TestCommonParser:
    """Tests for CommonParser."""

    def test_has_output_and_verbose_options(self):
        """CommonParser defines --output and --verbose."""
        parser = CommonParser()
        args = parser.parse_args([])
        assert args.output is None
        assert args.verbose is False

    def test_parses_output_and_verbose(self):
        """CommonParser parses -o/--output and --verbose."""
        parser = CommonParser()
        args = parser.parse_args(["-o", "out.json", "--verbose"])
        assert args.output == "out.json"
        assert args.verbose is True


class TestFromlocal:
    """Tests for fromlocal CLI."""

    def test_calls_from_local_with_parsed_args(self, tmp_path):
        """fromlocal parses argv and calls from_local with file and output."""
        src = tmp_path / "in.json"
        src.write_text('{"b": 1, "a": 2}', encoding="utf-8")
        dst = tmp_path / "out.json"
        with patch("sys.argv", ["json-sort-fromfile", str(src), "-o", str(dst)]):
            fromlocal()
        assert dst.exists()
        import json
        assert json.loads(dst.read_text(encoding="utf-8")) == {"a": 2, "b": 1}

    def test_verbose_calls_from_local(self, tmp_path):
        """fromlocal with --verbose still calls from_local."""
        src = tmp_path / "in.json"
        src.write_text("{}", encoding="utf-8")
        with patch("sys.argv", ["json-sort-fromfile", "--verbose", str(src)]):
            with patch("json_sort.scripts.from_local") as mock_fl:
                fromlocal()
        mock_fl.assert_called_once_with(src=str(src), dst=None)


class TestFromurl:
    """Tests for fromurl CLI."""

    def test_calls_from_remote_with_parsed_args(self):
        """fromurl parses argv and calls from_remote with url and output."""
        with patch("sys.argv", ["json-sort-fromremote", "https://example.com", "-o", "/tmp/out.json"]):
            with patch("json_sort.scripts.from_remote") as mock_fr:
                fromurl()
        mock_fr.assert_called_once_with(src="https://example.com", dst="/tmp/out.json")

    def test_fromurl_without_output_calls_with_none(self):
        """fromurl with no -o passes dst=None."""
        with patch("sys.argv", ["json-sort-fromremote", "https://api.example.com"]):
            with patch("json_sort.scripts.from_remote") as mock_fr:
                fromurl()
        mock_fr.assert_called_once_with(src="https://api.example.com", dst=None)
