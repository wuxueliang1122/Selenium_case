#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import sys
sys.path.append("D:\\Program Files\\python-workplace\\Python3\\")

from Selenium.Gensee.public import location, webplayersdk_login
from Selenium.Gensee.public.webplayersdk_login import LoginDemo, Element_location, Document_directory
import unittest, os, time, csv

class Gensee_SubmitQuestion(unittest.TestCase):

    def setUp(self):
        self.login = LoginDemo()
        self.element = Element_location()
        self.document = Document_directory()

        self.driver = self.login.flash_launch_firefox()
        self.driver.implicitly_wait(10)
        self.browser = location
        self.verificationErrors = []
        self.accept_next_alert = True
        self.login.login(self.driver) #登录sdk
        self.data_content = self.element.data_content(self.driver)
        self.msg_type = self.element.message_type(self.driver)
        self.time_interval = 0     #boss后台设置的提问间隔时间
        self.result_true = '"result":true'
        self.result_false = '"result":false'
        self.login.webuser_login(self.driver)  # 登录web用户
        self.handles = self.driver.window_handles

    #选择提问模块
    def submit(self):
        driver = self.driver
        browser = self.browser
        driver.switch_to_window(self.handles[0])
        submitQ_type = self.msg_type
        submitQ_type.find_element_by_xpath("//option[@value='submitQuestion']").click()

    #获取web用户接收到sdk用户发送的消息，需要开启自动发布问题给web用户
    """
        还有一个问题，问题越来越多，需要滚动条控制，但是现在还没实现能把滚动条滑到最底下然后获取最新接收到的问题，
        如果不滑到最低端应该是获取不到最新接收到的问题的。所以这个脚本还是有点问题的。
    """
    def get_ques_content_web(self):
        driver = self.driver
        driver.switch_to.window(self.handles[1])
        time.sleep(5)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(1)
        new_question = self.browser.findsClassName(self.driver, "auto_spac")[-1].text
        return new_question


    """所有条件都允许的情况下，submitquestion操作以及反应"""
    def test_submitquestion(self):
        driver = self.driver
        browser = self.browser

        driver.switch_to.window(self.handles[0])
        self.submit()
        time.sleep(2)
        send_button = self.element.send_button(driver) #获取“发送”按钮的定位
        submitQ_content = self.data_content  #获取“数据内容”窗口
        filename = self.document.document_dir() + "\\submitQuestion_content.csv"
        with open(filename, 'r') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                submitQ_content.clear()
                submitQ_content.send_keys(content)
                time.sleep(1)
                send_button.click()

                # 发送的消息与已发送模块中显示的一致
                sent_msg = browser.findXpath(driver, "//*[@id='sendedMsgDiv']/div/span")
                self.assertEqual(content[0], sent_msg.text)
                # logs显示的发送成功--
                # 发送成功会显示两条信息
                get_true_result = self.element.get_true_result(driver)
                self.assertEqual(self.result_true, get_true_result)
                web_get_content = self.get_ques_content_web()   #web端接收到的提问
#                self.assertEqual(content[0], constrast_content)  #输入格式和输出格式不一样，用if判断一下
                if web_get_content in content[0]:
                    pass
                else:
                    raise TypeError("error.")
                time.sleep(self.time_interval+1)
                #切换到sdk
                driver.switch_to.window(self.handles[0])
#                 print(receive_msg.text)   #flash没打开，没有加入直播  那是不是也要验证没加入直播提示是什么？？

    """当操作时间小于boss设置的提问间隔时间,boss间隔提问时间尽量设置的稍微大一点,submit_in_time 间隔时间内提问"""
    def test_submitq_in_time(self):
        driver = self.driver
        browser = self.browser
        self.submit()
        time.sleep(2)
        data_content = self.data_content
        send_msg = '{"content":"当发送问题时间小于boss设置的提问间隔时间验证"}'
        send_button = self.element.send_button(driver)

        now_time = time.strftime("%M%S", time.localtime(time.time()))
        interval_time = 0
        flag = True
        while interval_time < self.time_interval:
            data_content.clear()
            data_content.send_keys(send_msg)
            send_button.click()
            send_time = time.strftime("%M%S", time.localtime(time.time()))
            get_true_result = self.element.get_true_result(driver)
            get_false_result = self.element.get_false_result(driver)
            interval_time = int(send_time) - int(now_time)
            if flag == False:
                self.assertEqual(self.result_false, get_false_result)
            else:
                flag = False
                self.assertEqual(self.result_true, get_true_result)
            time.sleep(1)

    """
    def test_submit_out_time(self):
        driver = self.driver
        browser = self.browser
        Gensee_SubmitQuestion.submit(self)
        time.sleep(3)
        send_button = webplayersdk_login.send_button(driver)
        data_content = self.data_content
        filename = filename = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\" \
                              "Gensee\\documents\\submitQuestion_content.csv"
        with open(filename, 'r') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                data_content.clear()
                data_content.send_keys(content)
                send_button.click()
                #获取 result
                receive_msg_sucess = browser.findXpath(driver, "//*[@id='eventslog']/div[2]/span").text.split(",")[-1]
                receive_msg_s_result = receive_msg_sucess[:len(receive_msg_sucess)-1]
                self.assertEqual('"result":true', receive_msg_s_result)
                time.sleep(self.time_interval+1)
        time.sleep(2)
    """
    #其他用户提问，sdk收不到

    #组织者问题答复，这个好像不大能测啊 到时再看看


    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()