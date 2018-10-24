#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

import time,re
from Selenium.Gensee.public import location


def login(driver, url):
    driver.get(url)
    driver.maximize_window()
    we = location
    time.sleep(2)
    un = we.findId(driver, 'loginNameInput')
    un.clear()
    un.send_keys("admin@gensee.com")
    time.sleep(2)
    we.findId(driver, 'passwordInput').send_keys("888888")
    time.sleep(2)
    we.findXpath(driver, "//div[@class='serve-left']/div[2]/div[2]/table/tbody/tr[3]/td/img").click()
    time.sleep(2)

def quit_login_down(driver):
    we = location
    we.findXpath(driver, "//div[@class='serve-left']/div[2]/div[2]/table/tbody/tr/td/span[2]").click()
    time.sleep(2)

def quit_login_up(driver):
    we = location
    we.findXpath(driver, "/html/body/div[2]/div[1]/div[1]/div[2]/table/tbody/tr/td/span[2]").click()

if __name__ == '__main__':
    login()
