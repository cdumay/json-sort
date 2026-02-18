"""Unit tests for json_sort.lib."""
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from json_sort.lib import (
    NoSuchFile,
    file_exists,
    file_write,
    from_local,
    from_remote,
    oncritical,
)


class TestNoSuchFile:
    """Tests for NoSuchFile exception."""

    def test_is_exception(self):
        """NoSuchFile is raised with message and extra."""
        with pytest.raises(NoSuchFile) as exc_info:
            raise NoSuchFile(message="not found", extra={"path": "/foo"})
        assert getattr(exc_info.value, "message", str(exc_info.value)) == "not found"
        assert getattr(exc_info.value, "extra", {}) == {"path": "/foo"}


class TestOncritical:
    """Tests for oncritical."""

    def test_logs_and_exits_on_generic_exception(self):
        """oncritical logs str(exc) and calls sys.exit(1)."""
        with patch("json_sort.lib.sys.exit") as mock_exit:
            with patch("json_sort.lib.logging") as mock_log:
                oncritical(ValueError("bad value"))
        mock_log.critical.assert_called_once_with("bad value")
        mock_exit.assert_called_once_with(1)

    def test_logs_message_on_http_exception(self):
        """oncritical logs exc.message for HTTPException."""
        from werkzeug.exceptions import NotFound as WZNotFound

        class FakeHTTP(WZNotFound):
            """HTTPException with .message for lib compatibility."""

            def __init__(self):
                super().__init__(description="HTTP 404")
                self.message = "HTTP 404"  # noqa: B025

        with patch("json_sort.lib.sys.exit") as mock_exit:
            with patch("json_sort.lib.logging") as mock_log:
                oncritical(FakeHTTP())
        mock_log.critical.assert_called_once_with("HTTP 404")
        mock_exit.assert_called_once_with(1)


class TestFileExists:
    """Tests for file_exists."""

    def test_raises_nosuchfile_when_missing(self, tmp_path):
        """file_exists raises NoSuchFile when file does not exist."""
        missing = tmp_path / "missing.json"
        with pytest.raises(NoSuchFile) as exc_info:
            file_exists(str(missing))
        assert "missing" in getattr(exc_info.value, "message", str(exc_info.value))
        assert getattr(exc_info.value, "extra", {}).get("filename") == str(missing.resolve())

    def test_returns_resolved_path_when_exists(self, tmp_path):
        """file_exists returns realpath when file exists."""
        f = tmp_path / "f.json"
        f.write_text("{}")
        result = file_exists(str(f))
        assert result == str(f.resolve())


class TestFileWrite:
    """Tests for file_write."""

    def test_writes_to_file(self, tmp_path):
        """file_write writes JSON to file when dst is set."""
        out = tmp_path / "out.json"
        data = {"z": 1, "a": 2}
        file_write(str(out), data)
        assert out.read_text(encoding="utf-8") == json.dumps(
            data, ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ": ")
        )
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded == {"a": 2, "z": 1}

    def test_writes_to_stdout_when_dst_none(self, capsys):
        """file_write writes to stdout when dst is None."""
        data = {"a": 1}
        file_write(None, data)
        out, _ = capsys.readouterr()
        assert '"a": 1' in out
        assert json.loads(out) == data


class TestFromLocal:
    """Tests for from_local."""

    def test_loads_and_writes_sorted_to_file(self, tmp_path):
        """from_local reads file and writes sorted JSON to dst."""
        src = tmp_path / "in.json"
        src.write_text('{"b": 2, "a": 1}', encoding="utf-8")
        dst = tmp_path / "out.json"
        from_local(str(src), str(dst))
        assert json.loads(dst.read_text(encoding="utf-8")) == {"a": 1, "b": 2}

    def test_loads_and_writes_to_stdout(self, tmp_path, capsys):
        """from_local writes to stdout when dst is None."""
        src = tmp_path / "in.json"
        src.write_text("{}", encoding="utf-8")
        from_local(str(src), None)
        out, _ = capsys.readouterr()
        assert json.loads(out) == {}

    def test_calls_oncritical_on_oserror(self, tmp_path):
        """from_local calls oncritical when open() fails (e.g. OSError)."""
        # file_exists is called first and would raise NoSuchFile; we make it
        # return a path that does not exist so open() raises OSError
        with patch("json_sort.lib.file_exists", return_value=str(tmp_path / "nope.json")):
            with patch("json_sort.lib.oncritical") as mock_crit:
                from_local("dummy", None)
        mock_crit.assert_called_once()
        assert isinstance(mock_crit.call_args[0][0], OSError)

    def test_calls_oncritical_on_json_decode_error(self, tmp_path):
        """from_local calls oncritical on invalid JSON."""
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        with patch("json_sort.lib.oncritical") as mock_crit:
            from_local(str(bad), None)
        mock_crit.assert_called_once()
        assert isinstance(mock_crit.call_args[0][0], json.JSONDecodeError)


class TestFromRemote:
    """Tests for from_remote."""

    def test_fetches_and_writes_sorted_to_file(self, tmp_path):
        """from_remote writes response to dst."""
        with patch("json_sort.lib.RESTClient") as mock_client:
            mock_client.return_value.do_request.return_value = {"c": 3, "a": 1}
            dst = tmp_path / "out.json"
            from_remote("https://example.com/api", str(dst))
        assert json.loads(dst.read_text(encoding="utf-8")) == {"a": 1, "c": 3}
        mock_client.return_value.do_request.assert_called_once_with(
            method="GET", path=""
        )

    def test_fetches_and_writes_to_stdout(self, capsys):
        """from_remote writes to stdout when dst is None."""
        with patch("json_sort.lib.RESTClient") as mock_client:
            mock_client.return_value.do_request.return_value = {"x": 1}
            from_remote("https://example.com", None)
        out, _ = capsys.readouterr()
        assert json.loads(out) == {"x": 1}

    def test_calls_oncritical_on_exception(self):
        """from_remote calls oncritical when client raises."""
        with patch("json_sort.lib.RESTClient") as mock_client:
            mock_client.return_value.do_request.side_effect = ValueError("network")
            with patch("json_sort.lib.oncritical") as mock_crit:
                from_remote("https://example.com", None)
        mock_crit.assert_called_once()
        assert mock_crit.call_args[0][0].args[0] == "network"
