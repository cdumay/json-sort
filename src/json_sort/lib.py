#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core logic: load JSON from local file or remote URL and write sorted output.

.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>
"""
import logging
import sys
import os
import json

from cdumay_error.types import NotFound  # pylint: disable=import-error
from cdumay_rest_client.client import RESTClient  # pylint: disable=import-error
from werkzeug.exceptions import HTTPException


class NoSuchFile(NotFound):  # pylint: disable=too-few-public-methods
    """Exception raised when the requested file does not exist."""


def oncritical(exc: BaseException) -> None:
    """Log the exception as critical and exit with code 1.

    :param exc: The exception to log (HTTPException or any other).
    """
    if isinstance(exc, HTTPException):
        logging.critical(exc.message)
    else:
        logging.critical(str(exc))
    sys.exit(1)


def file_exists(filename: str) -> str:
    """Resolve and check that the given path exists; raise if not.

    :param filename: Path to the file.
    :type filename: str
    :returns: The resolved absolute path.
    :rtype: str
    :raises NoSuchFile: If the file does not exist.
    """
    filename = os.path.realpath(filename)
    logging.debug("Checking file: %s", filename)
    if not os.path.exists(filename):
        raise NoSuchFile(
            message=f"No such file '{filename}'",
            extra={"filename": filename}
        )
    return filename


def file_write(dst: str | None, data: object) -> None:
    """Write JSON data to a file or stdout with sorted keys.

    :param dst: Output path, or None to write to stdout.
    :type dst: str or None
    :param data: JSON-serializable data to write.
    """
    if dst:
        dst = os.path.realpath(dst)
        logging.debug("Saving to: %s", dst)
        with open(dst, "w", encoding="utf-8") as out:
            json.dump(
                data, out, ensure_ascii=False, sort_keys=True, indent=2,
                separators=(',', ': ')
            )
    else:
        logging.debug("Current std will be used")
        json.dump(
            data, sys.stdout, ensure_ascii=False, sort_keys=True, indent=2,
            separators=(',', ': ')
        )


def from_local(src: str, dst: str | None = None) -> None:
    """Load JSON from a local file and write it sorted to dst or stdout.

    :param src: Path to the input JSON file.
    :type src: str
    :param dst: Output path, or None for stdout.
    :type dst: str or None
    """
    try:
        with open(file_exists(src), "r", encoding="utf-8") as fhl:
            file_write(dst, json.load(fhl))
    except (OSError, json.JSONDecodeError) as exc:
        oncritical(exc)


def from_remote(src: str, dst: str | None = None) -> None:
    """Fetch JSON from a URL and write it sorted to dst or stdout.

    :param src: URL to fetch JSON from.
    :type src: str
    :param dst: Output path, or None for stdout.
    :type dst: str or None
    """
    try:
        file_write(
            dst, RESTClient(server=src).do_request(method="GET", path="")
        )
    except (OSError, TypeError, ValueError, HTTPException) as exc:
        oncritical(exc)
