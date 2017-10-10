#!/usr/bin/env python
# coding: utf-8
"""Python client library for the PCS API.
"""
from requests import Session
from . import version

__version__ = version.__version__


class YunApi(object):
    """A client for the PCS API.
    """
    def __init__(self, bduss, session=None, timeout=None):
        self.bduss = bduss
        self.session = session or Session()
        self.timeout = timeout

    def request(self, uri):
        pass


class YunApiError(Exception):
    """YunApiError
    """
    pass
