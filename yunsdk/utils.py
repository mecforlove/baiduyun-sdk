# coding: utf-8
from queue import Queue
from threading import Thread, Lock, current_thread

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
                 chunk=102400):
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

    def download(self):
        with open(self.save_path, 'wb') as fp:
            theads = []
            for i in range(self.thread_num):
                p = Thread(target=self._produce, name='%d' % i)
                theads.append(p)
                p.start()
            c = Thread(target=self._consume, args=(fp, ), name='consumer')
            theads.append(c)
            c.start()
            for t in theads:
                t.join()

    def _produce(self):
        while True:
            if self.mutex.acquire():
                if self.position > self.file_size - 1:
                    self.flags[int(current_thread().getName())] = True
                    self.mutex.release()
                    return
                interval = (self.position, self.position + self.chunk)
                self.position += (self.chunk + 1)
                self.mutex.release()
            resp = self.session.get(
                self.url, headers={'Range': 'bytes=%s-%s' % interval})
            if not self.queue.full():
                self.queue.put((interval, resp.content))

    def _consume(self, fp):
        while True:
            if all(self.flags) and self.queue.empty():
                return
            if not self.queue.empty():
                item = self.queue.get()
                fp.seek(item[0][0])
                fp.write(item[1])

    def _content_length(self):
        """发送head请求获取content-length
        """
        resp = self.session.head(self.url)
        length = resp.headers.get('content-length')
        if length:
            return int(length)
        else:
            raise Exception('%s don\'t support Range' % self.url)
