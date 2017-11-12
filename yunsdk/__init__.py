#!/usr/bin/env python
# coding: utf-8
"""Python client library for the PCS API.
"""
import os
import threading

from requests import Session
from . import version

__version__ = version.__version__
APP_ID = 266719  # The app_id of ES file explore on android.
BASE_URL = 'http://pcs.baidu.com/rest/2.0/pcs'


class YunApi(object):
    """A client for the PCS API.
    """

    def __init__(self, bduss, session=None, timeout=None):
        """

        :param budss: The value of baidu cookie key `BDUSS`.
        """
        self.bduss = bduss
        self.session = session or Session()
        self.timeout = timeout
        # Add core auth cookie
        self.session.headers.update({'Cookie': 'BDUSS=%s' % self.bduss})

    def quota(self):
        """空间配额信息"""

        return self.get('/quota', dict(method='info'))

    def download(self, yun_path, local_path=None):
        """下载文件

        当local_path为None时，文件会保存在工作目录下，文件名默认为网盘的文件名。
        当local_path以/结尾时，文件名默认为网盘的文件名
        :param yun_path: 网盘下的文件路径
        :param local_path: 保存本地的文件路径
        """
        yun_dir, yun_filename = os.path.split(yun_path)
        cwd = os.getcwd()
        if local_path is None:
            local_dir = cwd
            local_filename = yun_filename
        else:
            local_dir, local_filename = os.path.split(local_path)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            if not local_filename:
                local_filename = yun_filename
        local_path = os.path.join(local_dir, local_filename)
        contents = self.get('/file', dict(method='download', path=yun_path))
        with open(local_path, 'wb') as f:
            for chunk in contents:
                if chunk:
                    f.write(chunk)
        return True

    def get(self, uri, params):
        return self.request('GET', uri, params=params)

    def request(self,
                method,
                uri,
                params=None,
                data=None,
                files=None,
                stream=None):
        if params is None:
            params = {}
        params.update({'app_id': APP_ID})
        if params.get('method') == 'download':  # Enable stream.
            stream = True
        resp = self.session.request(
            method,
            BASE_URL + uri,
            params=params,
            data=data,
            files=files,
            timeout=self.timeout,
            stream=stream)
        # Support stream when download
        if stream:
            return resp.iter_content(chunk_size=1024)
        return resp.json()


class YunApiError(Exception):
    """YunApiError
    """
    pass
