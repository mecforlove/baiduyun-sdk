# baiduyun-sdk

This client library is designed to support the [BaiduYun PCS API](http://developer.baidu.com/wiki/index.php?title=docs/pcs), which is a way to manage your cloud files with Python.

SDK不包含用户登录认证的部分，所以在开始使用之前，必须获得百度帐号的合法cookie，这里不需要全部，只需要BDUSS。

首先，导入模块，创建网盘操纵的实例：
```python
>>> from yunsdk import YunApi
>>> yun = YunApi('your bduss value')
```
获得实例后，就可以使用相应的方法操纵网盘的文件：
- 下载
```python
>>> yun.download('/test.txt', 'test.txt')
```
第一个参数是云端路径，第二个参数是本地存储文件的路径。该下载方法采用了多线程，可以获得较为快速的下载体验。
- 删除
```python
>>> yun.delete('/test.txt')
```
- 上传
```python
>>> yun.upload('test.txt', '/test.txt', ondup=False)
```
第一个参数为本地待上传的文件路径，第二个为云端的存储路径，ondup参数控制覆盖行为，默认为True（覆盖已存在文件）。

- 移动
- 复制
- 离线
