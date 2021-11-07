# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:44:50 2021

@author: Charvi.Gaur
"""

import time
import pytesseract
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class DRTData:
    def __init__(self, drt, party):
        self.drt = drt
        self.party = party
        
    def scroll_height(self, driver, speed=90):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")
        
    def ReadImgCaptcha(self, driver, img):
        location = img.location
        size = img.size
        screenshotBytes = driver.get_screenshot_as_png()
        imageScreenshot = Image.open(BytesIO(screenshotBytes))
        imageScreenshot = imageScreenshot.crop((location['x'], location['y'] - 263, location['x'] + size['width'], location['y'] - 263 + size['height']))
        text = pytesseract.image_to_string(imageScreenshot).strip()
        return text
        """
        resp = requests.get(driver.find_element_by_class_name('imgcaptcha').get_attribute('src'))
        img = Image.open(io.BytesIO(resp.content))
        text = pytesseract.image_to_string(img).strip()
        """
        
    def scrapData(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1200")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get('https://drt.gov.in/front/page1_advocate.php')
        #Provide input to the page#
        #Selecting item from dropdown list and sending it
        if self.drt != "" or self.drt != None:
            select_element1 = ui.Select(ui.WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "schemaname"))))
            select_element1.select_by_visible_text(self.drt)
        #Enetering free text provided as input
        if self.party != "" or self.party != None:
            driver.find_element_by_id('name').send_keys(self.party)   
        #Detecting captcha
        self.scroll_height(driver)
        time.sleep(10)
        img = driver.find_element_by_xpath('//div[@class="row"]//img')
        captcha = self.ReadImgCaptcha(driver, img)
        driver.find_element_by_name('answer').send_keys(captcha)
        #Clicking on search
        driver.find_element_by_id('submit1').click()
        ####Now get data from the table
        tabdata = driver.find_element_by_xpath('//div[@class="row"]//div[@class="scroll-table1"]/table')
        tabsp = BeautifulSoup(tabdata.get_attribute('innerHTML'), 'lxml')
        dct = {}
        bodlst = []
        data = []
        headlst = [row.text.replace('\n','').strip() for header in tabsp.find_all('tr') for row in header.find_all('th')]
        for tbody in tabsp.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                for td in tr.find_all('td'):
                    bodlst.append(td.text.replace('\n', '').strip())
                dct = dict(zip(headlst, bodlst))
                data.append(dct)
        return data