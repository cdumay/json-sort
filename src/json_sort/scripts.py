#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI entry points for JSON sort (local file and URL).

.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>
"""
import logging
import argparse

from .lib import from_local, from_remote


class CommonParser(argparse.ArgumentParser):
    """Argument parser with common options: output file and verbosity."""

    def __init__(self, **kwargs) -> None:
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument(
            "--output", "-o", metavar="FILE",
            help="output file (default: stdout)"
        )
        self.add_argument(
            "--verbose", help="increase output verbosity", action="store_true"
        )


def fromlocal() -> None:
    """Parse CLI, then load JSON from a local file and output sorted."""
    parser = CommonParser()
    parser.add_argument("file", help="input file")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)-8s: %(message)s"
    )
    from_local(src=args.file, dst=args.output)


def fromurl() -> None:
    """Parse CLI, then fetch JSON from a URL and output sorted."""
    parser = CommonParser()
    parser.add_argument("url", help="url to fetch")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)-8s: %(message)s"
    )
    from_remote(src=args.url, dst=args.output)
