#coding=utf-8
import selenium
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import warnings
import os
from threading import Thread
from multiprocessing import Process

driver = webdriver.Chrome()
driver.set_window_size(1100,1220)

def snkrlogin(username,password):
    driver.get("https://www.nike.com/tw/launch/")
    element = WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/ul/li[3]/a'))
    #driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/ul/li[1]/button').click()
    #element = WebDriverWait(driver, 10).until(
        #lambda driver: driver.find_element_by_xpath('//*[@id="nike-unite-login-view"]/header/div[2]'))
    while True:
        try:
            driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/ul/li[1]/button').click()
            element = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_xpath('//*[@id="nike-unite-login-view"]/header/div[2]'))
            us = driver.find_element_by_xpath("//input[@name='emailAddress']").send_keys(username)
            ps = driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
            time.sleep(2)
            lb =driver.find_element_by_xpath("//input[@value='登入']").click()
            time.sleep(3)
            if driver.find_element_by_xpath('//li[text()="很抱歉，目前無法連接到伺服器。 請稍後再試。"]') or driver.find_element_by_xpath('//li[text()="您的電子郵件或密碼輸入不正確"]'):
                print("無法登入 請檢查")
                driver.refresh()
                time.sleep(5)
        except:
            print("Sucess")
            break

def getproduct(producturl):
    buttonxpath = "//button[@data-qa='add-to-cart']"
    driver.get(producturl)
    element = WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div[1]/div/div[3]/div[2]/div/section[1]/div[2]/aside/div/div[1]/h5'))
    driver.execute_script("window.scrollTo(0, 750)")
    element = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath(buttonxpath))
    try:
        driver.find_element_by_xpath(buttonxpath)
        print("還有尺寸 嘗試加車")
    except(NoSuchElementException):
        print("Sold Out!!")


def addtocart(username,password,producturl):
    buttonxpath = "//button[@data-qa='add-to-cart']"
    snkrlogin(username,password)
    getproduct(producturl)
    while True:
        element = WebDriverWait(driver, 20).until(
            lambda driver: driver.find_element_by_xpath("//button[@data-qa='size-dropdown']"))
        try:
            driver.find_element_by_xpath("//button[text()='CM 27']").click()
            print("點擊尺寸")
            try:
                clickadd = driver.find_element_by_xpath(buttonxpath).click()
                print("正在加入購物車")
                element = WebDriverWait(driver, 5).until(
                    lambda driver: driver.find_element_by_xpath("//h3[text()='已加入購物籃']"))
                if driver.find_element_by_xpath("//h3[text()='已加入購物籃']"):
                    print("加入購物車成功")
                    driver.get("https://www.nike.com/tw/cart")
                else:
                    print("加入購物車失敗")
            except:
                print("無法加入購物車,再試一次")
                return clickadd
        except:
            print("尺寸無法點選 請更改")
            break


if __name__ == "__main__":
    addtocart('username', 'password','producturl')
