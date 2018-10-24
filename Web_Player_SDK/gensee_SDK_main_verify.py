#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import sys
sys.path.append("D:\\Program Files\\python-workplace\\Python3\\")
from Selenium.Gensee.public import location,webplayersdk_login
from Selenium.Gensee.public.webplayersdk_login import LoginDemo, Element_location, Document_directory


import unittest, os, time

class Gensee_Main_Verify(unittest.TestCase):
    def setUp(self):
        self.driver = LoginDemo().flash_launch_firefox()
        self.driver.implicitly_wait(10)
        self.browser = location
        self.verificationErrors = []
        self.accept_next_alert = True
        LoginDemo().login(self.driver)

    def test_send_message(self):
        driver = self.driver
        browser = self.browser
        message_type_standard = \
        ["submitQuestion", "submitRollcall", "submitAttention", "submitUpgrade", "submitVote", "submitChat", "submitChatTo",
         "submitMute", "submitVolume", "submitOpenVideo", "requireNetSettings", "submitNetChoice", "applyUpgrade",
          "submitStop", "submitHandup", "submitUsername", "submitShowVideoCover", "submitPlay",
         "submitPause", "submitStream", "submitSpeedReport", "submitReward"]
        data_content_standard =  '{"content":"what\'s your name?"}'
        message_types = driver.find_elements_by_xpath("//*[@id='test_event_type_select']/option")
        print(len(message_types))
        for i in range(len(message_types)):
            self.assertEqual(message_type_standard[i], message_types[i].get_attribute('value'))
            data_content = driver.find_element_by_xpath("//*[@id='test_message_textarea']").text
            self.assertEqual(data_content_standard, data_content)

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()