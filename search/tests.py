from django.test import TestCase

# Create your tests here.
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Search(unittest.TestCase):
    def setUp(self):
        chromedriver = "C:/Users/Jaimes/Desktop/chromedriver.exe"
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_search(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        driver.find_element_by_xpath("//input[@value='Search']").click()
        driver.find_element_by_name("q").click()
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("-1")
        driver.find_element_by_xpath("//input[@value='Search']").click()
        driver.find_element_by_name("q").click()
        driver.find_element_by_name("q").click()
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("dolores")
        driver.find_element_by_name("q").send_keys(Keys.ENTER)
        driver.find_element_by_name("dropdown").click()
        Select(driver.find_element_by_name("dropdown")).select_by_visible_text("Garbage")
        driver.find_element_by_name("dropdown").click()
        driver.find_element_by_xpath("//input[@value='Search']").click()
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("")
        driver.find_element_by_xpath("//input[@value='Search']").click()
        driver.find_element_by_name("q").click()
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("-1")
        driver.find_element_by_xpath("//input[@value='Search']").click()
        driver.find_element_by_xpath("//img").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    # Added tests
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == "__main__":
    unittest.main()
