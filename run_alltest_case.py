# coding=utf-8

from selenium import webdriver

import unittest
import time
import HTMLTestRunner

import sys
sys.path.append("D:\\Program Files\\python-workplace\\Python3\\")

def testSuite():
    listcase = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\Gensee\\Web_Player_SDK"

    testunit = unittest.TestSuite()

    discover = unittest.defaultTestLoader.discover(listcase,
                                    pattern="gensee*.py",
                                    top_level_dir=None)

    for testcase in discover:
        testunit.addTest(testcase)
    return testunit

if __name__ == '__main__':

    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    filename = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\TestLogs\\Gensee_Logs\\" + now_time + ".html"
    with open(filename, 'wb') as fp:



        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title="Gensee测试报告",
            description="测试用例运行情况")
        testunit = testSuite()
        runner.run(testunit)
