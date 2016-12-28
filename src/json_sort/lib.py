#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import sys, os, json
from cdumay_rest_client.client import RESTClient
from cdumay_rest_client.exceptions import NotFound, HTTPException


class NoSuchFile(NotFound):
    """NoSuchFile"""


def oncritical(exc):
    """description of oncritical"""
    if isinstance(exc, HTTPException):
        logging.critical(exc.message)
    else:
        logging.critical(str(exc))
    sys.exit(1)


def file_exists(filename):
    """description of file_exists"""
    filename = os.path.realpath(filename)
    logging.debug("Checking file: {}".format(filename))
    if not os.path.exists(filename):
        raise NoSuchFile(
            message="No such file '{}'".format(filename),
            extra=dict(filename=filename)
        )
    return filename


def file_write(dst, data):
    """description of file_write"""
    if dst:
        dst = os.path.realpath(dst)
        logging.debug("Saving to: {}".format(dst))
        out = open(dst, "w")
    else:
        logging.debug("Current std will be used")
        out = sys.stdout

    json.dump(
        data, out, ensure_ascii=False, sort_keys=True, indent=2,
        separators=(',', ': ')
    )


def from_local(src, dst=None):
    """description of from_local"""
    try:
        file_write(dst, json.load(open(file_exists(src), "r")))
    except Exception as exc:
        oncritical(exc)


def from_remote(src, dst=None):
    """description of fromurl"""
    try:
        file_write(
            dst, RESTClient(server=src).do_request(method="GET", path="")
        )
    except Exception as exc:
        oncritical(exc)
