# coding: utf-8
from queue import Queue
from threading import Thread

from requests import head, get


class SuperDownloader(object):
    """HTTP下载较大文件的工具
    """

    def __init__(self, url, session, save_path, thread_num=10, queue_size=10):
        """

        :param url: 资源链接
        :param session: 构造好上下文的session
        :param save_path: 保存路径
        :param thread_num: 下载线程数
        :param queue_size: 队列的大小，默认10
        """
        self.url = url
        self.session = session
        self.save_path = save_path
        self.thread_num = thread_num
        self.queue= Queue(queue_size)
        self.file_size = self._content_length()

    def download(self):
        pass

    def _produce(self):
        pass

    def _consume(self):
        pass

    def _content_length(self):
        """发送head请求获取content-length
        """
        resp = self.session.head(self.url)
        length = resp.headers.get('content-length')
        if length:
            return int(length)
        else:
            raise Exception('%s don\'t support Range')
