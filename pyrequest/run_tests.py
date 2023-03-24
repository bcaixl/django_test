import time
import sys
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data
sys.path.append('./interface')
sys.path.append('./db_fixture')


# 指定测试用例为当前目录下的interface文件夹
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')


if __name__ == '__main__':
    test_data.init_data()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    file_name = './report/' + now + '_result.html'
    fp = open(file_name, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Guest Manage System Interface Test Report',
                            description='Implementation Example with:'
                            )
    runner.run(discover, 0, False)
    fp.close()
