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

chromedriver_path = '<your_chromedriver.exe_path>'

class ChromePark(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(chromedriver_path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_chrome_park(self):
        driver = self.driver
        driver.get("http://35.230.88.48/")
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("head")
        driver.find_element_by_name("q").send_keys(Keys.ENTER)
        self.assertEqual("Heron's Head Park", driver.find_element_by_xpath("//div/div[2]/p/strong").text)
        self.assertEqual("April 24, 2018, 9:52 a.m.", driver.find_element_by_xpath("//div/div[2]/p[2]/strong").text)
        self.assertEqual("Bathroom", driver.find_element_by_xpath("//p[3]/strong").text)
        self.assertEqual("Weird toilet signs", driver.find_element_by_xpath("//p[4]/strong").text)
        self.assertEqual("Park: Heron's Head Park", driver.find_element_by_xpath("//div[2]/div[2]/p").text)
        self.assertEqual("Date: April 24, 2018, 9:56 a.m.", driver.find_element_by_xpath("//div[2]/div[2]/p[2]").text)
        self.assertEqual("Category: Medical Waste", driver.find_element_by_xpath("//div[2]/div[2]/p[3]").text)
        self.assertEqual("Issue: Park is entirely giant pills", driver.find_element_by_xpath("//div[2]/div[2]/p[4]").text)
    
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

if __name__ == "__main__":
    unittest.main()

class ChromeInvalid(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chromedriver_path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_chrome_invalid(self):
        driver = self.driver
        driver.get("http://35.230.88.48/")
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("-1234")
        driver.find_element_by_name("q").send_keys(Keys.ENTER)
        self.assertEqual("Please enter alphanumeric characters only. Search either by zip code, park name or city name.", driver.find_element_by_xpath("//p[2]").text)
    
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

if __name__ == "__main__":
    unittest.main()

class ChromeSimilar(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chromedriver_path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_chrome_similar(self):
        driver = self.driver
        driver.get("http://35.230.88.48/")
        Select(driver.find_element_by_name("dropdown")).select_by_visible_text("Bathroom")
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys("94110")
        driver.find_element_by_name("q").send_keys(Keys.ENTER)
        self.assertEqual("No parks matched your zip code, here are reports that share the bathroom category.", driver.find_element_by_xpath("//p[2]").text)
    
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

if __name__ == "__main__":
    unittest.main()
