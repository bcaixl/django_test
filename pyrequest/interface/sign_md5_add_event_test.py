import unittest
import hashlib
import requests
import os
import time
import sys
from db_fixture import test_data
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


class AddEventTest(unittest.TestCase):
    """加了签名鉴权的发布会增加测试"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        # api_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_request_error(self):
        """请求办法错误"""
        r = requests.get(self.base_url)
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'request error')

    def test_add_event_sign_null(self):
        """签名参数为空"""
        payload = {'eid': 1, 'name': '', 'limit': 2000, 'address': '', 'start_time': '', 'time': '', 'sign': ''}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user sign null')

    def test_add_event_sign_timeout(self):
        """签名超时"""
        now_time = str(int(str(self.client_time)) - 30)
        payload = {'eid': 1, 'name': '', 'limit': 2000, 'address': '', 'start_time': '', 'time': now_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10013)
        self.assertEqual(result['message'], 'user sign timeout')

    def test_add_event_sign_error(self):
        """签名错误"""

        payload = {'eid': 1, 'name': '', 'limit': 2000, 'address': '', 'start_time': '', 'time': self.client_time,
                   'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10014)
        self.assertEqual(result['message'], 'user sign error')

    def test_add_event_sign_success(self):
        """签名错误"""

        payload = {'eid': 31, 'name': '黑加仑1号', 'limit': 2000, 'address': '广州越秀', 'start_time': '2025-01-01 09:00:00',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')


if __name__ == '__main__':
    unittest.main()
