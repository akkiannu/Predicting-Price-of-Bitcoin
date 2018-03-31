
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
import bs4


# In[2]:


def extract_historical_data(driver):
    data_div = driver.find_element_by_css_selector('.table')
    head =[t.text for t in data_div.find_elements_by_tag_name('th')]
    #print(head)
    contentlist = []
    for t in data_div.find_elements_by_tag_name('tr'):
        row_list = []
        for r in t.find_elements_by_tag_name('td'):
            row_list.append(r.text)
        #row_list_t = tuple(row_list)
        contentlist.append(row_list)
    #print(contentlist)
    DF = pd.DataFrame.from_records(contentlist, columns=head)
    return DF


# In[4]:


driver = webdriver.Firefox(executable_path='geckodriver.exe')
driver.get('https://coinmarketcap.com/')
bitcoin_bar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#id-verge > td:nth-child(2) > a:nth-child(3)')))
bitcoin_bar.click()
normal_delay = random.normalvariate(3, 0.5)
time.sleep(normal_delay)
his_info = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[5]/div[1]/ul/li[5]/a')
his_info.click()
normal_delay = random.normalvariate(3, 0.5)
time.sleep(normal_delay)
period_select = driver.find_element_by_css_selector('#reportrange')
period_select.click()
normal_delay = random.normalvariate(3, 0.5)
time.sleep(normal_delay)
period = driver.find_element_by_css_selector('.ranges > ul:nth-child(1) > li:nth-child(4)')
period.click()
normal_delay = random.normalvariate(3, 0.5)
time.sleep(normal_delay)
XVGcoin_record = extract_historical_data(driver)


# In[5]:



XVGcoin_record.to_csv('XVG_price.csv')


# In[6]:


XVGcoin_record

