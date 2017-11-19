# coding: utf-8
import unittest

import yunsdk


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