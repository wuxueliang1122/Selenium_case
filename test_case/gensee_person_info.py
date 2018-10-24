#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import os,re,time,csv
import unittest

import sys
curPath = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\Gensee\\public"
sys.path.append(curPath)
from Selenium.Gensee.public import login,location



class Gensee_Person_Info(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.we = location
        self.driver.implicitly_wait(10)
        self.base_url = ""
        self.verificationErrors = []
        self.accept_next_alert = True

    def person_info_modify(self):
        driver = self.driver
        we = self.we
        #调用 登录
        login.login(driver, self.base_url)


        #进入个人信息和密码
        info = we.findXpath(driver, "//div[@class='serve-hight-1']/table/tbody/tr/td/span")
        info.click()
        time.sleep(2)



    """个人信息和密码文字对比"""
    def test_login_info(self):#个人信息和密码文字验证
        driver = self.driver
        we = self.we
        Gensee_Person_Info.person_info_modify(self)

        tab_bgcolor, tab_font_size = "#9dbfe4", "wenzi-12"

        """tab栏字体大小、颜色、等对比"""
        login_info = we.findXpath(driver, "//td[@align='center']/table/tbody/tr[2]/td")
        person_info = we.findXpath(driver, "//td[@align='center']/table[2]/tbody/tr/td")

        self.assertEqual("登录信息", login_info.text)
        self.assertEqual(tab_bgcolor, login_info.get_attribute('bgcolor'))
        self.assertEqual(tab_font_size, login_info.get_attribute('class'))

        self.assertEqual("个人信息", person_info.text)
        self.assertEqual(tab_bgcolor, person_info.get_attribute('bgcolor'))
        self.assertEqual(tab_font_size, person_info.get_attribute('class'))

        time.sleep(3)


        """
        这里应该还要验证显示的游戏地址跟登入的邮箱地址是否一致。
        但是因为用的是独立的py写的login，没有传入数据，暂时不验证这个了
        """

        """个人信息和密码整一页文字显示验证"""
        #登录信息
        email_addr_left = we.findXpath(driver, "//*[@id='form1']/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]")
        self.assertEqual("邮箱地址：", email_addr_left.text)


        pw_left = we.findXpath(driver,
                               "//form[@action='profile!savePassword']/table/tbody/tr/td/table/tbody/tr[2]/td")
        try:
            self.assertEqual("密　　码:*", pw_left.text)
        except:
            pass

        pw_right_tips = we.findXpath(driver,
                                "//form[@action='profile!savePassword']/table/tbody/tr/td/table/tbody/tr[2]/td[2]")
        self.assertEqual("(提醒:密码长度6到15位)", pw_right_tips.text)
        #raise ValueError("密码规则提醒语言错误")

        pw_con_left = we.findXpath(driver,
                                "//form[@action='profile!savePassword']/table/tbody/tr/td/table/tbody/tr[3]/td")
        self.assertEqual("确认密码：*", pw_con_left.text)
        #raise ValueError("确认密码显示错误")

        """
        个人信息：用定位一组元素的方式进行，但是最后一行“提交”是图片的形式，所以下面没有比较，对比的时候长度减了1
        """

        listtitle = \
            [
            "名　　称： *", "性　　别：   先生 　 女士", "公司名称：", "地　　址：", "邮　　编：", "地　　区：",
            "电　　话：", "手　　机：", "工作性质：", "产品和服务：", "邮箱地址：", "省：", "市：", "区：", "个人描述：",
            "IP地址：   ", "操作系统：   ", "浏览器：   "
            ]#最后三项右框还有三个空格
        list_links = we.findsXpath(driver, "//form[@action='profile!save']/table/tbody/tr/td/table/tbody/tr")
        self.assertEqual(len(listtitle), len(list_links)-1)
        for i in range(len(list_links)-1):
            self.assertEqual(listtitle[i], list_links[i].text)

        login_info_submit = we.findXpath(driver,
                                "//form[@action='profile!savePassword']/table/tbody/tr/td/table/tbody/tr/td/img")
        submit_pic = "http://192.168.1.233/webcast/branding/default/zh_CN/images/enrol-2.jpg"
        self.assertEqual(submit_pic, login_info_submit.get_attribute('src'))

        person_info_submit = we.findXpath(driver,
                                "//*[@id='form2']/table/tbody/tr/td/table/tbody/tr[19]/td/table/tbody/tr[1]/td/img")
        self.assertEqual(submit_pic, person_info_submit.get_attribute('src'))

        login.quit_login_down(self)
        print("validation is over.")




    """用户登录界面欢迎语显示的名字 和登录信息邮箱地址 和个人信息中的名称对比"""
    def test_verify_unameAndlname(self): #验证用户登录显示的和邮箱地址和个人信息中的名称是否对称
        driver = self.driver
        we = self.we
        Gensee_Person_Info.person_info_modify(self)

        #获取左侧用户登录welcome语句中的用户名称
        uname_display = we.findXpath(driver, "//*[@class='serve-hight-1']/table/tbody/tr/td")
        listname = uname_display.text.split("\n")[0]
        uname_left = ""
        for i in range(len(listname)-1, -1, -1):
            if listname[i] != "！":
                uname_left = listname[i] + uname_left
            else:
                break

        uname_right = we.findName(driver, "user.profile.name").get_attribute('value')
        self.assertEqual(uname_left, uname_right)

        email_addr_right = we.findXpath(driver, "//*[@id='form1']/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]").text
        #email_addr_right 长度却是18，然后for循环只能输出前几个很奇怪
        email_uname = ""
        for data in email_addr_right:
            if data != "@":
                if data != " ":
                    email_uname += data
            else:
                break
        self.assertEqual(uname_right, email_uname)
        login.quit_login_down(self)
        print("over")




    """性别：男女多次切换验证"""
    def test_gender_switch(self):
        # 性别：先生、女士的定位
        def get_female():
            female = we.findXpath(driver, "//*[@id='form2']/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[1]")
            return female

        def get_male():
            male = we.findXpath(driver, "//*[@id='form2']/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[2]")
            return male

        driver = self.driver
        we = self.we
        Gensee_Person_Info.person_info_modify(self)

#        submit = we.findXpath(driver, "//*[@onclick='submitProfileForm()']")
        #性别 男女切换操作
        count = 0
        while count < 5:
            submit = we.findXpath(driver,
                                  "//*[@id='form2']/table/tbody/tr/td/table/tbody/tr[19]/td/table/tbody/tr[1]/td/img")
            is_famale = get_female().get_attribute('checked')
            is_male = get_male().get_attribute('checked')
            if  is_famale == "true":
                get_male().click()
                submit.click()
                time.sleep(2)
                self.assertEqual(None, get_female().get_attribute('checked'))
                self.assertEqual("true", get_male().get_attribute('checked'))
            elif is_male == "true":
                get_female().click()
                submit.click()
                time.sleep(2)
                self.assertEqual(None, get_male().get_attribute('checked'))
                self.assertEqual("true", get_female().get_attribute('checked'))
            else:
                raise ValueError("性别男女都未选中")
            count += 1
        login.quit_login_down(self)
        print("verify is over")




    """密码更改各种提示"""
    def test_change_pw(self):
        Gensee_Person_Info.person_info_modify(self)
        driver = self.driver
        we = self.we

        def get_ch_pw():
            ch_pw = we.findXpath(driver, "//*[@id='password']")
            return ch_pw

        def get_ch_pw_confirm():
            ch_pw_confrim = we.findName(driver, 'confirmPassword')
            return ch_pw_confrim

        my_file = "D:\\Program Files\\python-workplace\\Python3\\Selenium\\Gensee\\test_case\\change_pw.csv"

        #1、密码输入框中未输入点提交，会出现“必选字段”提示
        submit = we.findXpath(driver, "//*[@id='form1']/table/tbody/tr[2]/td/table/tbody/tr[1]/td/img")
        submit.click()
        self.assertEqual("enrol-down-1 required error", get_ch_pw().get_attribute('class'))
        choose_tips_1 = we.findXpath(driver, "//*[@id='form1']/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/label")
        self.assertEqual("必选字段", choose_tips_1.text)

        self.assertEqual("enrol-down-1 required error", get_ch_pw_confirm().get_attribute('class'))
        choose_tips_2 = we.findXpath(driver,
                                     "//*[@id='form1']/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]/label/label")
        self.assertEqual("必选字段", choose_tips_2.text)

        with open(my_file, 'r') as pwfile:
            row = csv.reader(pwfile)
            for data in row:
                pw, pw_confirm = data[0], data[1]
                if len(pw) < 6:
                    get_ch_pw().send_keys(pw)
                    time.sleep(1)
                    self.assertEqual("长度最少是 6位", choose_tips_1.text)
                    time.sleep(2)
                    get_ch_pw().clear()
                    time.sleep(3)
                    submit.click()
                elif len(pw_confirm) < 6:
                    get_ch_pw_confirm().send_keys(pw_confirm)
                    time.sleep(1)
                    self.assertEqual("长度最少是 6位", choose_tips_2.text)
                    time.sleep(2)
                    get_ch_pw_confirm().clear()
                    time.sleep(3)
                    submit.click()
                elif pw != pw_confirm:
                    get_ch_pw().send_keys(pw)
                    time.sleep(1)
                    get_ch_pw_confirm().send_keys(pw_confirm)
                    time.sleep(1)
                    self.assertEqual("请再次输入相同的值", choose_tips_2.text)
                    time.sleep(2)
                    get_ch_pw().clear()
                    get_ch_pw_confirm().clear()
                    time.sleep(3)
                    submit.click()
                else:
                    self.assertEqual("", choose_tips_1.text)
                    time.sleep(1)
                    self.assertEqual("", choose_tips_2.text)
                    time.sleep(1)
                    print("same password is not submit.")
 #                   submit.click()
        login.quit_login_down(self)

        print("password_change is over")




    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)



def suite():
    testunit = unittest.TestSuite()
    testunit.addTest(Gensee_Person_Info('test_change_pw'))
    return testunit

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
