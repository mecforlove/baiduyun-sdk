# coding: utf-8
import os
import unittest

import yunsdk

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__)) + '/test.txt'
YUN_PATH = '/test.txt'
YUN_DIR_PATH = '/test'


class YunApiTestCase(unittest.TestCase):
    def setUp(self):
        try:
            with open('tests/.BDUSS', 'r') as fp:
                self.bduss = fp.readline()
        except IOError:
            raise Exception('.BDUSS file must exist in test directory.')
        self.client = yunsdk.YunApi(bduss=self.bduss)


class TestQuota(YunApiTestCase):
    def test_quota(self):
        ret = self.client.quota()
        self.assertIn('quota', ret)
        self.assertIn('used', ret)


class TestUpload(YunApiTestCase):
    def test_upload(self):
        import tempfile
        local_path = tempfile.mkstemp()[1]
        yun_path = '/test.txt'
        with open(local_path, 'wb') as tmp_fp:
            file_content = 'hello'
            tmp_fp.write(file_content)
        ret = self.client.upload(local_path, yun_path)
        self.assertEqual(ret['path'], yun_path)
        self.assertEqual(ret['size'], 5)
        self.assertEqual(ret['isdir'], 0)


class TestDelete(YunApiTestCase):
    def test_delete_file(self):
        self.client.upload(LOCAL_PATH, YUN_PATH)
        ret = self.client.delete(YUN_PATH)
        self.assertIn('request_id', ret)


class TestMkdir(YunApiTestCase):
    def test_mkdir(self):
        self.client.delete(YUN_DIR_PATH)
        ret = self.client.mkdir(YUN_DIR_PATH)
        self.assertEqual(ret['path'], YUN_DIR_PATH)
        self.assertEqual(ret['isdir'], 1)
        self.client.delete(YUN_DIR_PATH)


class TestDownload(YunApiTestCase):
    def test_download(self):
        self.client.upload(LOCAL_PATH, YUN_PATH)
        os.remove(LOCAL_PATH)
        ret = self.client.download(YUN_PATH, LOCAL_PATH)
        self.assertTrue(ret)
        