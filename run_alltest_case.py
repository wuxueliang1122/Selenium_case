# coding=utf-8

from selenium import webdriver

import unittest
import time
import HTMLTestRunner

import os
dir_path = os.getcwd()

def testSuite():
    listcase = dir_path + "\\Selenium_case\\Web_Player_SDK"

    testunit = unittest.TestSuite()

    discover = unittest.defaultTestLoader.discover(listcase,
                                    pattern="gensee*.py",
                                    top_level_dir=None)

    for testcase in discover:
        testunit.addTest(testcase)
    return testunit

if __name__ == '__main__':

    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    filename = dir_path + "Selenium_case\\test_case" + now_time + ".html"
    with open(filename, 'wb') as fp:



        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title="Web UI测试报告",
            description="测试用例运行情况")
        testunit = testSuite()
        runner.run(testunit)
