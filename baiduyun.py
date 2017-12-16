#!/usr/bin/env python2

### usage: ./baiduyun.py download /remote/path/file  /local/path/file
###        ./baiduyun.py delete /remote/path/file
###        ./baiduyun.py upload /local/path/file  /remote/path/file
### you must specify the file name, it can't be a directory
### put your BDUSS into file BDUSS at the same level with this script
### if the file is more than 600M, this script will not work,
### but you can split the file to make sure it's less than 600M

import sys
from yunsdk import YunApi
bduss = open("BDUSS",'r')
yun = YunApi(bduss.readline()[:-1])

if sys.argv[1] == "download":
    yun.download(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "delete":
    yun.delete(sys.argv[2])
elif sys.argv[1] == "upload":
    yun.upload(sys.argv[2], sys.argv[3], ondup=False)
else:
    print("unknow parameter: " + sys.argv[1])



