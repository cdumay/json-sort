"""Pytest configuration and fixtures.

Injects minimal mocks for cdumay_error, cdumay_rest_client and werkzeug
so tests can run when those packages are not installed (e.g. CI).
"""
import sys
from types import ModuleType


def _install_mock_modules():
    """Install mock modules so json_sort can be imported without full deps."""
    if "cdumay_error" in sys.modules:
        return

    class NotFound(Exception):
        """Minimal NotFound for tests."""

        def __init__(self, message=None, extra=None):
            super().__init__(message)
            self.message = message
            self.extra = extra or {}

    cdumay_error = ModuleType("cdumay_error")
    cdumay_error_types = ModuleType("cdumay_error.types")
    cdumay_error_types.NotFound = NotFound
    cdumay_error.types = cdumay_error_types
    sys.modules["cdumay_error"] = cdumay_error
    sys.modules["cdumay_error.types"] = cdumay_error_types

    class RESTClient:
        """Minimal RESTClient for tests."""

        def __init__(self, server=None):
            self.server = server

        def do_request(self, method=None, path=None):
            return {}

    cdumay_rest_client = ModuleType("cdumay_rest_client")
    cdumay_rest_client_client = ModuleType("cdumay_rest_client.client")
    cdumay_rest_client_client.RESTClient = RESTClient
    cdumay_rest_client.client = cdumay_rest_client_client
    sys.modules["cdumay_rest_client"] = cdumay_rest_client
    sys.modules["cdumay_rest_client.client"] = cdumay_rest_client_client

    try:
        import werkzeug.exceptions  # noqa: F401
    except ImportError:
        class HTTPException(Exception):
            """Minimal HTTPException for tests."""
            message = ""

        class NotFound(HTTPException):
            """Minimal NotFound for tests."""

        werkzeug = ModuleType("werkzeug")
        werkzeug_exceptions = ModuleType("werkzeug.exceptions")
        werkzeug_exceptions.HTTPException = HTTPException
        werkzeug_exceptions.NotFound = NotFound
        werkzeug.exceptions = werkzeug_exceptions
        sys.modules["werkzeug"] = werkzeug
        sys.modules["werkzeug.exceptions"] = werkzeug_exceptions


_install_mock_modules()
