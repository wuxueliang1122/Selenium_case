#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select
from selenium.common.exceptions import NoSuchElementException

from Selenium.Gensee.public import location,login

import unittest,os,time

class Gensee_Onging_Lives(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.we = location
        self.driver.implicitly_wait(10)
        self.base_url = "http://192.168.1.233/webcast"
        self.verificationErrors = []
        self.accept_next_alert = True
    def search_bar(self):
        search_bar = self.we.findName(self.driver, "webcast.subject")
        return search_bar
    def search_button(self):
        search_button = self.we.findXpath(self.driver, "//*[@id='searchForm']/input[2]")
        return search_button
    def ongoing_interface(self):
        ongoing_interface = self.we.findXpath(self.driver, "/html/body/div[2]/div[2]/div[2]/div[2]")
        return ongoing_interface

    def test_text_comparison(self):
        driver = self.driver
        we = self.we
        login.login(driver, self.base_url)

        #进入“正在进行”
        we.findPLinkText(driver, "正在进行").click()

        #搜索栏tips显示
        search_bar_tips = "请在此输入您想要查找的主题信息"
        search_bar = Gensee_Onging_Lives.search_bar(self)
        self.assertEqual(search_bar_tips, search_bar.get_attribute('value'))
        time.sleep(1)

        #搜索栏点入之后value值会消失，显示空白
        search_bar.click()
        self.assertEqual("", search_bar.get_attribute('value'))
        time.sleep(1)

        #没有正在进行的直播tips显示
        ongoing_interface_tips = "请根据关键字搜索，不输入任何关键字搜索，将加载所有已公开的直播列表"
        ongoing_interface = Gensee_Onging_Lives.ongoing_interface(self)
        self.assertEqual(ongoing_interface_tips, ongoing_interface.text)

        #搜索栏空白 点击搜索 tips会显示
        Gensee_Onging_Lives.search_button(self).click()
        print(search_bar.get_attribute('value'))
        self.assertEqual(search_bar_tips, Gensee_Onging_Lives.search_bar(self).get_attribute('value'))

        print("verify is over")

    def test_search_blank(self):
        driver = self.driver
        we = self.we
        login.login(driver, self.base_url)

        we.findPLinkText(driver, "正在进行").click()

        search_bar = Gensee_Onging_Lives.search_bar(self)
        search_button = Gensee_Onging_Lives.search_button(self)
        search_bar_tips = "请在此输入您想要查找的主题信息"
        search_bar.click()
        time.sleep(1)

        # 空白点击搜索后bar_tips又会显示
        search_button.click()
        self.assertEqual(search_bar_tips, Gensee_Onging_Lives.search_bar(self).get_attribute('value'))
        time.sleep(1)
        #只要点过搜索main页面tips不再显示,显示页码
        self.assertEqual("- 1/1 -", Gensee_Onging_Lives.ongoing_interface(self).text)
        print("verify is over_2")

    def test_search(self):
        driver = self.driver
        we = self.we
        login.login(driver, self.base_url)
        search_bar = Gensee_Onging_Lives.search_bar(self)
        search_button = Gensee_Onging_Lives.search_button(self)
        search_bar.clear()
        search_bar.send_keys("Mikasa")
        time.sleep(1)
        search_button.click()
        time.sleep(2)

        #直播主题内容对比
        live_content_standard = ["直播主题", "开始时间", "内容介绍"]
        




        print("verify is over_3")

if __name__ == '__main__':
    unittest.main()
