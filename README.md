# baiduyun-sdk

This client library is designed to support the [BaiduYun PCS API](http://developer.baidu.com/wiki/index.php?title=docs/pcs), which is a way to manage your cloud files with Python.

> login登录来自[SpiderClub](https://github.com/SpiderClub/smart_login/tree/master/baidu/login_direct.py)

首先，导入模块，获取bduss,创建网盘操纵的实例：
```python
>>> from yunsdk import YunApi
>>> from yunsdk import GetBduss
>>> bduss = GetBduss("username","password")
>>> yun = YunApi(bduss)
```
得实例后，就可以使用相应的方法操纵网盘的文件：
- 列出目录文件
```python
yun.list('/我的资源')
```
```
+---------+-------------------------------------------------+-------+----------+
| 文件夹: |                    我的资源                     | 大小: |    0     |
+=========+=================================================+=======+==========+
| 文件夹: |                       abc                       | 大小: |    0     |
+---------+-------------------------------------------------+-------+----------+
| 文件名: |      音效Boom 2_v1.6.2_[密钥：osx.cx].dmg       | 大小: | 14048256 |
+---------+-------------------------------------------------+-------+----------+
| 文件名: | 腾讯视频破解版-1.4.0登陆任意账号VIP视频随便看.dmg | 大小: | 14534304 |
+---------+-------------------------------------------------+-------+----------+
| 文件名: |                翻墙 VPN Plus.zip                | 大小: |  543353  |
+---------+-------------------------------------------------+-------+----------+
```
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

---------------------------------------------------------------------
or:
    下载
    $./baiduyun.py download /remote/path/file  /local/path/file

    上传
    $./baiduyun.py upload /local/path/file  /remote/path/file

    删除
    $./baiduyun.py delete /remote/path/file

文件大小不能超过600M,上传或者下载前请先确定文件大小，或者分割文件后再操作
   split -b 590M file-name the-suffix-you-want
eg. split -b 590M video.mp4 video.
    cat video.a* > new.video.mp4 合并成新的文件 
