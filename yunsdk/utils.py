# coding: utf-8
from queue import Queue
from threading import Thread, Lock, current_thread, active_count

from requests import head, get


class SuperDownloader(object):
    """HTTP下载较大文件的工具
    """

    def __init__(self,
                 url,
                 session,
                 save_path,
                 thread_num=45,
                 queue_size=10,
                 chunk=10240):
        """

        :param url: 资源链接
        :param session: 构造好上下文的session
        :param save_path: 保存路径
        :param thread_num: 下载线程数
        :param queue_size: 队列的大小，默认10
        :param chunk: 每个线程下载的块大小
        """
        self.url = url
        self.session = session
        self.save_path = save_path
        self.thread_num = thread_num
        self.queue = Queue(queue_size)
        self.file_size = self._content_length()
        self.position = 0  # 当前的字节偏移量
        self.chunk = chunk
        self.mutex = Lock()  # 资源互斥锁
        self.flags = [False] * self.thread_num
        self.fp = open(save_path, 'wb')

    def download(self):
        for i in range(self.thread_num):
            Thread(target=self._produce, name='%d' % i).start()
        Thread(target=self._consume, name='consumer').start()

    def _produce(self):
        while True:
            if self.mutex.acquire():
                if self.position > self.file_size - 1:
                    self.flags[int(current_thread().getName())] = True
                    self.mutex.release()
                    break
                interval = (self.position, self.position + self.chunk)
                self.position += (self.chunk + 1)
                self.mutex.release()
            resp = self.session.get(
                self.url, headers={'Range': 'bytes=%s-%s' % interval})
            self.queue.put((interval, resp.content))

    def _consume(self):
        while True:
            if active_count() == 2:
                break
            if not self.queue.empty():
                item = self.queue.get()
                self.fp.seek(item[0][0])
                self.fp.write(item[1])
        self.fp.close()

    def _content_length(self):
        """发送head请求获取content-length
        """
        resp = self.session.head(self.url)
        length = resp.headers.get('content-length')
        if length:
            return int(length)
        else:
            raise Exception('%s don\'t support Range' % self.url)
