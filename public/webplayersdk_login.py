#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import sys
sys.path.append("D:\\Program Files\\python-workplace\\Python3\\")

from Selenium.Gensee.public import location
import time, os, re
class LoginDemo():
    def __init__(self):
        self.browser = location

        self.base_url = "http://192.168.1.233"
        self.id = "4d1dc05507c047c2a4e2ba2baa209ff4"
        self.authcode = "000000"
        self.ctx_training = "training"
        self.ctx_webcast = "webcast"
        self.uid = self.sdk_uid()
        self.uname = self.sdk_uname()

    def sdk_uid(self):
        sdk_uid = "9999999999"
        return sdk_uid

    def sdk_uname(self):
        sdk_uname = "selenium_sdk"
        return sdk_uname

    def web_uid(self, driver):
        web_uid = self.browser.findXpath(driver,
                    "//*[@class='gs-sdk-widget']").get_attribute('uid')
        return web_uid

    #Firefox浏览器启动时修改配置为flash自启动
    def flash_launch_firefox(self):
        """
        option = webdriver.FirefoxProfile()
        option.set_preference("plugin.state.flash", 2)
        driver = webdriver.Firefox(option)

        :return:
        """
        chromeOpitons = Options()
        prefs = {

            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

        }

        chromeOpitons.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chromeOpitons)

        return driver

    def login(self, driver):
        browser = self.browser

        sdk_url = self.base_url + "/sdk/site/test/simple?ownerid=" \
                  + self.id + "&authcode=" + self.authcode + "&ctx=" + self.ctx_webcast + "&uid=" + self.uid \
                  + "&uname=" + self.uname
        driver.get(sdk_url)
        driver.maximize_window()

        time.sleep(5)

    def webuser_login(self, driver):
        browser = self.browser
        username = "selenium_web"
        password = "000000"
        #        driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL + "t")
        js = 'window.open("http://192.168.1.233/webcast/site/entry/join-4d1dc05507c047c2a4e2ba2baa209ff4")'
        driver.execute_script(js)
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        un = browser.findXpath(driver, "//*[@id='nickNameInput']")  # 获取用户名框定位
        pw = browser.findCss(driver, "input#tokenInput")  # 获取密码框定位
        sub = browser.findXpath(driver, "//*[@class='submit-form']/button")  # 进入直播
        un.clear()
        un.send_keys(username)
        time.sleep(1)
        pw.clear()
        pw.send_keys(password)
        time.sleep(1)
        sub.click()
        time.sleep(5)

class Element_location():
    def __init__(self):
        self.browser = location
    #消息类型
    def message_type(self, driver):
        browser = self.browser
        msg_type = browser.findXpath(driver, "//*[@id='test_event_type_select']")
        return msg_type
    #数据内容
    def data_content(self, driver):
        browser = self.browser
        data_content = browser.findXpath(driver, "//*[@id='test_message_textarea']")
        return data_content
    #“发送”按钮
    def send_button(self, driver):
        browser = self.browser
        send_button = browser.findXpath(driver, "//input[@class='btn btn-primary']")
        return send_button
    #发送成功接收到的消息，“来自title”那一条
    def receive_msg_success(self, driver):
        browser = self.browser
        receive_success = browser.findXpath(driver, "//*[@id='eventslog']/div[2]/span")
        return receive_success
    #发送失败接收到的信息
    def receive_msg_failure(self, driver):
        browser = self.browser
        receive_failure = browser.findXpath(driver, "//*[@id='eventslog']/div[1]/span")
        return receive_failure
    #发送成功接收到的信息，result=true
    def get_true_result(self, driver):
        browser = self.browser
        receive_msg_s_text = self.receive_msg_success(driver).text.split(",")[-1]
        true_result = receive_msg_s_text[:len(receive_msg_s_text)-1]
        return true_result
    #发送失败接收到的信息，result=false
    def get_false_result(self, driver):
        browser = self.browser
        receive_msg_f_text = self.receive_msg_failure(driver).text.split(",")[-1]
        false_result = receive_msg_f_text[:len(receive_msg_f_text)-1]
        return false_result

class Document_directory():
    #数据驱动的目录
    def document_dir(self):
        filename = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\Gensee\\documents"
        return filename


