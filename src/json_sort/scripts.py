#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import argparse
from .lib import from_local, from_remote


class CommonParser(argparse.ArgumentParser):
    """CommonParser"""

    def __init__(self, **kwargs):
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.add_argument(
            "--output", "-o", metavar="FILE",
            help="output file (default: stdout)"
        )
        self.add_argument(
            "--verbose", help="increase output verbosity", action="store_true"
        )


def fromlocal():
    """description of fromlocal"""
    parser = CommonParser()
    parser.add_argument("file", help="input file")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)-8s: %(message)s"
    )
    from_local(src=args.file, dst=args.output)


def fromurl():
    """description of fromurl"""
    parser = CommonParser()
    parser.add_argument("url", help="url to fetch")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)-8s: %(message)s"
    )
    from_remote(src=args.url, dst=args.output)
