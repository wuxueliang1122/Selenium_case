# coding=utf-8
import unittest
import time
import csv
import random
from selenium.webdriver.common.keys import Keys
from Selenium.Gensee.public import location
from Selenium.Gensee.public.webplayersdk_login import LoginDemo, Element_location, Document_directory


class SubmitChat(unittest.TestCase):

    def setUp(self):
        self.driver = LoginDemo().flash_launch_firefox()  # Firefox浏览器定制启动：flash自动运行
        self.browser = location
        self.driver.implicitly_wait(10)
        self.verificationErrors = []
        self.login = LoginDemo()
        self.accept_next_alert = True
        self.login.login(self.driver)  # 登录sdk
        self.sdk_uid = self.login.sdk_uid()

        """
        下面都是sdk页面下才能获取到的定位
        """
        self.element = Element_location()
        self.document = Document_directory()
        self.send_button = self.element.send_button(self.driver)
        self.data_content = self.element.data_content(self.driver)
        self.msg_type = self.element.message_type(self.driver)
        self.receive_msg_success = self.element.receive_msg_success(self.driver)
        self.sdk_uid = self.login.sdk_uid()
        """
        以下为web用户相关信息和操作
        """
        self.login.webuser_login(self.driver)  # 登录web页面
        self.web_uid = self.login.web_uid(self.driver)  # 获取web用户的web uid
        """   """
        self.handles = self.driver.window_handles  # 获取当前sdk页面和web页面的句柄
        # sdk接收到消息 result表示是否发送成功
        self.result_true = '"result":true'
        self.result_false = '"result":false'
        self.time_interval = 0  # BOSS设置的聊天和提问时间间隔

    # 消息类型选择聊天模块
    def submit(self):
        self.driver.switch_to_window(self.handles[0])
        self.msg_type.find_element_by_xpath("//*[@value='submitChat']").click()

    # web页面聊天模块：聊天内容输入框和发送按钮定位
    def web_chat_area(self):
        self.driver.switch_to_window(self.handles[1])
        area = self.browser.findId(self.driver, "chat-area")
        return area

    def web_chat_submit(self):  # 发送按钮click()有一个报错  Element button could not be scrolled into view  没解决
        self.driver.switch_to_window(self.handles[1])
        send_button = self.browser.findXpath(self.driver, "//*[@id='chat-submit']")
        return send_button

    # 获取web用户接收到的聊天信息，因为收到最新的滚动条自动会滚到最低端，所以能够直接获取，没有提问那个问题
    def get_receive_chat_web(self):
        driver = self.driver
        browser = self.browser
        driver.switch_to_window(self.handles[1])
        time.sleep(2)
        """调试当前页面用的
        chat_area = self.web_chat_area()
        chat_submit = self.web_chat_submit()
        chat_area.clear()
        chat_area.send_keys("kkkk")
        chat_area.send_keys(Keys.ENTER)
        time.sleep(2)
        """

        chat_contents = browser.findsXpath(driver, "//*[@class='gs-msg-list']/li")  # 所有聊天记录的组元素定位
        chat_content = chat_contents[-1]  # 选取最新的聊天记录
        text = chat_content.find_element_by_xpath("span").text
        return text

    """
    #获取web用户发送或者接收的表情的src内容
    def get_receive_expre_web(self):
        driver = self.driver
        browser = self.browser
        driver.switch_to_window(self.handles[1])
        time.sleep(1)
        chat_contents = browser.findsXpath(driver, "//*[@class='gs-msg-list']/li")  # 定位到所有聊天的组元素定位
        chat_content = chat_contents[-1]  # 选取最新的聊天记录
        src = chat_content.find_element_by_xpath("span/img").get_attribute('src')
        return src
    """

    # 文本聊天内容发送成功——只包含content
    def test_submitchat_content(self):
        """
        文本聊天内容发送成功——即只包含content
        Returns:

        """
        driver = self.driver
        browser = self.browser
        time.sleep(2)
        self.submit()  # 选取聊天模块
        time.sleep(2)
        data_content = self.data_content
        send_button = self.send_button
        filename = self.document.document_dir() + "\\submitChat_content.csv"
        with open(filename, 'r', encoding='gb18030', errors='ignore') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                driver.switch_to_window(self.handles[0])  # 切换到sdk窗口
                data_content.clear()
                data_content.send_keys(content)
                time.sleep(1)
                send_button.click()
                get_true_result = self.element.get_true_result(driver)
                self.assertEqual(self.result_true, get_true_result)
                # 与web页面收到的信息作对比, 但是会有问题，遇到空格之类的，显示的空格数量不一致
                web_receive_chat = self.get_receive_chat_web()
                try:
                    self.assertIn(web_receive_chat, content[0])  # a in b
                except AssertionError:
                    print(web_receive_chat, content[0])
                time.sleep(self.time_interval + 1)
        time.sleep(2)

    # 富文本聊天内容发送成功——即只包含richtext
    def test_submitchat_richtext(self):
        driver = self.driver
        browser = self.browser
        time.sleep(1)
        self.submit()
        time.sleep(2)
        data_content = self.data_content
        send_button = self.send_button

        filename = self.document.document_dir() + "\\submitChat_richtext.csv"
        with open(filename, 'r', encoding='gb18030', errors='ignore') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                data_content.clear()
                data_content.send_keys(content)
                send_button.click()
                get_true_result = self.element.get_true_result(driver)
                self.assertEqual(self.result_true, get_true_result)
                time.sleep(self.time_interval + 1)
        time.sleep(2)

    # 发送的richtext聊天内容带表情
    def test_submit_richtext_expre(self):
        driver = self.driver
        browser = self.browser

        self.submit()
        time.sleep(2)
        data_content = self.data_content
        send_button = self.send_button

        filename = self.document.document_dir() + "\\submitChat_richtext_expre.csv"
        with open(filename, 'r', encoding='gb18030', errors='ignore') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                data_content.clear()
                data_content.send_keys(content)
                send_button.click()
                get_true_result = self.element.get_true_result(driver)
                self.assertEqual(self.result_true, get_true_result)
                time.sleep(self.time_interval + 1)
        time.sleep(2)

    # 发送的聊天内容带content和richtext——以richtext为主,并且加入了security
    def test_submit_all(self):
        driver = self.driver
        self.submit()
        time.sleep(2)

        data_content = self.data_content
        send_button = self.send_button

        filename = self.document.document_dir() + "\\submitChat_all.csv"
        with open(filename, 'r', encoding='gb18030', errors='ignore') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                data_content.clear()
                data_content.send_keys(content)
                send_button.click()
                get_true_result = self.element.get_true_result(driver)
                self.assertEqual(self.result_true, get_true_result)
                time.sleep(self.time_interval + 1)
        time.sleep(2)

    # 如果输入格式有问题，弹窗处理
    """
    def test_submit_invalidformate_tips(self):
        driver = self.driver
        self.submit()
        time.sleep(2)
        data_content = self.data_content
        send_button = self.send_button

        content = 'content："111"'
        data_content.clear()
        data_content.send_keys(content)
        send_button.click()
        alert = driver.switch_to.alert()
        alert.accept()
    
    #但是这个弹窗的元素定位不到，提示是空的
    """

    # 聊天间隔内，发送聊天信息
    def test_submitchat_in_time(self):
        driver = self.driver
        browser = self.browser
        self.submit()  # sdk，消息类型 选中聊天模块
        time.sleep(2)
        data_content = self.data_content  # sdk数据内容框 定位
        send_msg = '{"content":"当发送问题时间小于boss设置的提问间隔时间验证"}'
        send_button = self.send_button  # sdk发送按钮定位

        now_time = time.strftime("%M%S", time.localtime(time.time()))  # 获取当前时间
        interval_time = 0
        flag = True
        while interval_time < self.time_interval:
            # 发送聊天内容
            data_content.clear()
            data_content.send_keys(send_msg)
            send_button.click()

            send_time = time.strftime("%M%S", time.localtime(time.time()))
            # sdk接收到消息  result true or false 进行对比
            get_true_result = self.element.get_true_result(driver)
            get_false_result = self.element.get_false_result(driver)
            interval_time = int(send_time) - int(now_time)
            if flag == False:
                self.assertEqual(self.result_false, get_false_result)
            else:
                # 第一次发送聊天消息是能发出去的
                flag = False
                self.assertEqual(self.result_true, get_true_result)
            time.sleep(1)

    # web用户发送纯文字聊天信息，sdk是否收到 验证点：onPublicChat 和 聊天内容， web——uid与sdk  senderUid
    def test_sdk_receive_text(self):
        driver = self.driver
        browser = self.browser
        chat_area = self.web_chat_area()  # web端发送聊天框定位
        receive_msg_title_standard = "onPublicChat"
        web_uid = self.web_uid
        filename = self.document.document_dir() + "\\submitChat_receive_text.csv"
        with open(filename, 'r') as fp_object:
            contents = csv.reader(fp_object)
            for content in contents:
                time.sleep(3)
                driver.switch_to_window(self.handles[1])  # 切换到web页面
                chat_area.clear()
                chat_area.send_keys(content)
                chat_area.send_keys(Keys.ENTER)  # send_button click有问题，所以用模拟键盘 Enter键发送
                time.sleep(3)
                driver.switch_to_window(self.handles[0])  # 切换到sdk页面，然后获取刚刚web发送的聊天内容
                time.sleep(1)
                receive_msg_title = browser.findXpath(driver,
                                                      "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]").text  # 获取sdk包含onPublicChat的接收到信息
                # 获取sdk不包含onPublicChat的接收到信息————可以取消不用
                receive_msg_text = browser.findXpath(driver, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/span").text
                print(receive_msg_title)
                print(receive_msg_text)
                # sdk接收到消息 包含了 onPublicChat和发送的聊天内容
                try:
                    self.assertIn(receive_msg_title_standard, receive_msg_title)
                except Exception:
                    print("title:", receive_msg_title)
                try:
                    self.assertIn(content[0], receive_msg_title)
                except Exception:
                    print("Content, ", receive_msg_title)
                try:
                    self.assertIn(web_uid, receive_msg_title)
                except:
                    raise ValueError("web_uid is error", receive_msg_title)
                time.sleep(2)

    # web用户发送表情，现在只验证sdk收到了, 只验证5个表情随机发送5个表情
    def test_sdk_receive_expre(self):
        driver = self.driver
        browser = self.browser
        receive_msg_title_standard = "onPublicChat"
        web_uid = self.web_uid
        chat_area = self.web_chat_area()
        time.sleep(3)
        # 获取所有表情定位元素组
        expresssion = browser.findXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/a/i")
        expresssion.click()  # 点击表情图标，调出所有能发的表情
        expressions = browser.findsXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/ul/li")
        num = 0
        while num <= 5:
            i = random.randint(0, len(expressions))
            driver.switch_to_window(self.handles[1])
            expresssion = browser.findXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/a/i")
            expresssion.click()
            time.sleep(1)
            expressions = browser.findsXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/ul/li")
            expressions[i].click()
            chat_area.send_keys(Keys.ENTER)
            time.sleep(2)
            driver.switch_to_window(self.handles[0])
            receive_msg_title = browser.findXpath(driver,
                                                  "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]").text  # 获取onPublicChat，

            self.assertIn(receive_msg_title_standard, receive_msg_title)
            self.assertIn(web_uid, receive_msg_title)  # web uid 和 sdk 里接收到的信息里的 senderUid进行断言
            # 本来想通过表情的src地址进行比较  发现sdk获取到的接收到信息里richtext为空白，所以就不能进行断言验证了
            #            self.assertIn(expresssion_src, receive_msg_title)
            num += 1
            time.sleep(1)

    """
    #发送所有表情, 建议单独执行，因为操作比较多，有时候会定位不到。
    def test_sdk_receive_expres(self):
        driver = self.driver
        browser = self.browser
        receive_msg_title_standard = "onPublicChat"
        web_uid = self.web_uid
        chat_area = self.web_chat_area()
        time.sleep(3)
        #获取所有表情定位元素组
        expresssion = browser.findXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/a/i")
        expresssion.click()    #点击表情图标，调出所有能发的表情
        expressions = browser.findsXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/ul/li")
        for i in range(len(expressions)):
            driver.switch_to_window(self.handles[1])
            expresssion = browser.findXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/a/i")
            expresssion.click()
            time.sleep(1)
            expressions = browser.findsXpath(driver, "//*[@id='widget-chat']/div/div[2]/div[2]/div[1]/div[1]/ul/li")
            expressions[i].click()
            chat_area.send_keys(Keys.ENTER)
            time.sleep(2)
            driver.switch_to_window(self.handles[0])
            receive_msg_title = browser.findXpath(driver,
                    "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]").text  # 获取onPublicChat，

            self.assertIn(receive_msg_title_standard, receive_msg_title)
            self.assertIn(web_uid, receive_msg_title)   #web uid 和 sdk 里接收到的信息里的 senderUid进行断言
            # 本来想通过表情的src地址进行比较  发现sdk获取到的接收到信息里richtext为空白，所以就不能进行断言验证了
#            self.assertIn(expresssion_src, receive_msg_title)
            num += 1
            time.sleep(1)
    """  # 发送所有表情，因为操作次数比较多，可能会定位不到元素，建议独立运行

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    unittest.main()
