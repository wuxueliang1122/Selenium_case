#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import time,os,re
import unittest
import HTMLTestRunner

class LoginDemo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://192.168.1.233/webcast"
        self.verificationErrors = []
        self.accept_next_alter = True

    def test_login(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        sleep(2)

        un = driver.find_element_by_id("loginNameInput")
        un.clear()
        un.send_keys("admin@gensee.com")
        pw = driver.find_element_by_id("passwordInput")
        pw.clear()
        pw.send_keys("888888")
        sleep(2)
        driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[3]/td/img").click()
        sleep(2)

    def test_getUserLogs(self):
        #用户日志
        driver = self.driver
        driver.find_element_by_xpath("//div[@class='serve-hight']/div[4]/a").click()
        """
        driver.find_element_by_xpath("//div[@id='menuDiv']/div[2]/div[3]/a").click()
        print("already user logs")
        sleep(2)
        """

        #录制件管理
        driver.find_element_by_xpath("//div[@class='serve-left']/div[2]/div[5]/div[1]/img").click()
        driver.find_element_by_xpath("//div[@class='serve-left']/div[2]/div[5]/div[2]/div/a").click()
        sleep(2)

        all_dianbo = driver.find_element_by_tag_name("_blank")
        storages = 0
        for dianbo in all_dianbo:
            storage = dianbo.find_element_by_xpath("//div[@class='serve-right-2']/table[2]/tr[2]/td[8]").text
            storages += storage
        print(storages)


    def test_exit(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        sleep(2)

        print("input username and password")
        un = driver.find_element_by_id("loginNameInput")
        print(un.get_attribute('type'))
        un.clear()
        un.send_keys("admin@gensee.com")
        pw = driver.find_element_by_id("passwordInput")
        pw.clear()
        pw.send_keys("888888")
        sleep(2)
        driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[3]/td/img").click()
        print("login successful")
        sleep(2)
        #退出
        driver.find_element_by_xpath("//td[@class='corporation-test']/span[2]").click()
        sleep(2)

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)


def testSuite():
    testunit = unittest.makeSuite(LoginDemo)
    return testunit

if __name__ == '__main__':
    now_time = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    filename = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\TestLogs\\" + now_time + "_gensee.html"
    fp = open(filename, 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u"gensee测试报告",
        description=u"用例执行情况"
    )

    runner.run(testSuite())
    fp.close()