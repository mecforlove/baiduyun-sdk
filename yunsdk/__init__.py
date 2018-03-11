#!/usr/bin/env python2
# coding: utf-8
"""Python client library for the PCS API.
"""
import os
import threading
import urllib
import requests
import sys
import json

from requests import Session

from .datatable import Table
from . import version
from .utils import SuperDownloader
from .login import GetBduss

reload(sys)
sys.setdefaultencoding('utf-8')

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
        params = {
            'method': 'download',
            'app_id': APP_ID,
            'path': yun_path
        }
        if sys.version_info.major == 3:
            query_string = urllib.parse.urlencode(params)
        else:
            query_string = urllib.urlencode(params)

        url = BASE_URL + '/file?%s' % query_string
        super_downloader = SuperDownloader(url, self.session, local_path)
        super_downloader.download()
        return True

    def upload(self, local_path, yun_path, ondup=True):
        """上传文件

        :param local_path: 本地文件路径
        :param yun_path: 云端文件路径
        :param ondup: 是否覆盖同名文件，默认覆盖
        """
        if ondup:
            ondup = 'overwrite'
        else:
            ondup = 'newcopy'
        params = {'method': 'upload', 'path': yun_path, 'ondup': ondup}
        files = {yun_path: open(local_path, 'rb')}
        return self.request('POST', '/file', params=params, files=files)

    def mkdir(self, yun_path):
        """创建目录

        :param yun_path: 云端文件夹路径
        """
        params = {'method': 'mkdir', 'path': yun_path}
        return self.request('POST', '/file', params=params)

    def delete(self, yun_path):
        """删除文件或者目录

        :param yun_path: 云端文件路径
        """
        params = {'method': 'delete', 'path': yun_path}
        return self.request('POST', '/file', params=params)
    def list(self, yun_path, by='name'):
        params = {'method': 'list', 'path': yun_path, 'by': by}
        response = self.request('GET', '/file', params=params)
        filelist = response[u'list']
        dirlist=[]
        doclist=[]
        for i in filelist:
            if i[u'isdir'] == 0:
                doclist.append(["文件名:",i[u'server_filename'],"大小:",str(i[u'size'])])
            else:
                doclist.append(["文件夹:",i[u'server_filename'],"大小:",str(i[u'size'])]) 
        if sys.version_info.major == 3:
            print(Table(4,dirlist + doclist))
        else:
            print Table(4,dirlist + doclist)
    def get(self, uri, params):
        return self.request('GET', uri, params=params)

    def request(self,
                method,
                uri,
                headers=None,
                params=None,
                data=None,
                files=None,
                stream=None):
        if params is None:
            params = {}
        params.update({'app_id': APP_ID})
        resp = self.session.request(
            method,
            BASE_URL + uri,
            headers=headers,
            params=params,
            data=data,
            files=files,
            timeout=self.timeout,
            stream=stream)
        return resp.json()


class YunApiError(Exception):
    """YunApiError
    """
    pass
