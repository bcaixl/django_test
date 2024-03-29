import unittest
import requests
import os
import sys
from db_fixture import test_data
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


class AddEventTest(unittest.TestCase):
    """添加发布会"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    def tearDown(self):
        print(self.result)

    def test_add_event_all_null(self):
        """所有参数都为空"""
        payload = {'eid': '', 'name': '', 'limit': '', 'address': '', 'start_time': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_id_exist(self):
        """id已存在"""
        payload = {'eid': 1, 'name': 'yijia', 'limit': 2000, 'address': 'guangzhou', 'start_time': '2023-05-01 00:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        """name已存在"""
        payload = {'eid': 11, 'name': '红米Pro发布会', 'limit': 2000, 'address': 'guangzhou',
                   'start_time': '2023-05-01 00:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name is already exists')

    def test_add_event_date_error(self):
        """日期错误"""
        payload = {'eid': 11, 'name': '黑米Pro发布会', 'limit': 2000, 'address': 'guangzhou',
                   'start_time': '2029'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error', self.result['message'])

    def test_add_event_success(self):
        """添加成功"""
        payload = {'eid': 11, 'name': '黑米Pro发布会', 'limit': 2000, 'address': 'guangzhou',
                   'start_time': '2024-01-01 09:00:00'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    test_data.init_data()
    print("数据初始化完毕！！！")
    unittest.main()
