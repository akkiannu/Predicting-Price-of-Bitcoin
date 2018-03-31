import time
import random
from selenium import webdriver
import csv
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import bs4
import pandas as pd
data_val = []
data_head = []
driver = webdriver.Firefox(executable_path =r'.\geckodriver.exe')
driver.get('https://coinmarketcap.com/currencies/verge/')
time.sleep(random.normalvariate(3,0.5))
driver.find_element_by_css_selector('.nav-tabs > li:nth-child(5) > a:nth-child(1)').click()
time.sleep(random.normalvariate(3,0.5))
driver.find_element_by_id('reportrange').click()
time.sleep(random.normalvariate(2,0.5))
driver.find_element_by_css_selector('.ranges > ul:nth-child(1) > li:nth-child(6)').click()

wait = WebDriverWait(driver,10)
data_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.table-responsive')))
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html,'html5lib')
for tr in soup.tbody.findAll('tr'):
    row = [td.text for td in tr.findAll('td')]
    data_val.append(row)
for th in soup.thead.tr.findAll('th'):
    if len(data_head)<len(data_val[0]):
        data_head.append(th.text)
    else:
        break
df =  pd.DataFrame(data_val, columns=data_head)
df.to_csv('prices_xvg.csv')



