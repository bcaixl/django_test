import requests
import unittest


class GetEventListTest(unittest.TestCase):
    """发布会查询接口测试"""

    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        """发布会id为空"""
        r = requests.get(self.url, params={"eid": ""})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        """发布会id错误"""
        r = requests.get(self.url, params={'eid': '901'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_success(self):
        """发布会查询成功"""
        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')


if __name__ == '__main__':
    unittest.main()

# # 查询发布会接口
# url = "http://127.0.0.1:8000/api/get_event_list"
# r = requests.get(url, params={'eid': 1})
# result = r.json()
# print(result)
#
# # 断言结果
# assert result['status'] == 200
# assert result['message'] == "success"
# assert result['data']['name'] == "小米100发布会"
# assert result['data']['address'] == "广州体育馆"
# assert result['data']['start_time'] == "2023-02-25 11:48:22"
