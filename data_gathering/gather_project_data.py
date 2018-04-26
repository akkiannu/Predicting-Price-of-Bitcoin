from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import random
import time
from bs4 import BeautifulSoup
normal_delay = random.uniform(0.5, 1.5)
import pymongo
import bs4
import pandas as pd
client = pymongo.MongoClient('localhost')
db = client['BTC']
#for stable concern, this scrape only scraper 2 days then close drive scrpe another two days
#cmd for get data from mongodb data base:
#cd C:\Program Files\MongoDB\Server\3.6\bin
#mongoexport --db dbname --collection collectionname --out traffic.json
#mongoexport --db XVG --collection twitters --out datagathered.json
from datetime import datetime, timedelta, date

def gen_daterange(year, month, day, days):
    start_date = date(year, month, day)
    end_date = start_date + timedelta(days)
    return [ start_date + timedelta(n) for n in range(0,int((end_date - start_date).days),2)]
# this function will scrape twitter and store in mongodb database
def scrape_twitter(start, end, word):
    search_url = "https://twitter.com/search?q=%22%23{}%22%20since%3A{}%20until%3A{}&src=typd"
    browser = webdriver.Firefox(executable_path=r'geckodriver.exe')
    browser.get(search_url.format(word,start,end))
    time.sleep(normal_delay)
    height_now = browser.execute_script("return document.body.scrollHeight")#compare the height after scroll
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if height_now == new_height:
            break
        else:
            height_now = new_height
    tweets = browser.find_elements_by_class_name('stream-item')
    twitter_list = []

    for tweet in tweets:
        temp_tweet_html = tweet.get_attribute('innerHTML')
        temp_one_twitter = BeautifulSoup(temp_tweet_html, "html.parser")
        try:
            text = temp_one_twitter.find("div",{"class":"js-tweet-text-container"}).text.strip()
            twitter_time = temp_one_twitter.find("a",{"class":"tweet-timestamp js-permalink js-nav js-tooltip"})['title'].split('-')[-1].strip()
            reply = temp_one_twitter.find('div', {"class":"ProfileTweet-action ProfileTweet-action--reply"})
            reply_num = reply.find('span',{"class":"ProfileTweet-actionCountForPresentation"}).text
            retweet = temp_one_twitter.find('div', {"class":"ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt"})
            retweet_num = retweet.find('span',{"class":"ProfileTweet-actionCountForPresentation"}).text
            favorite = temp_one_twitter.find('div', {"class":"ProfileTweet-action ProfileTweet-action--favorite js-toggleState"})
            favorite_num = favorite.find('span',{"class":"ProfileTweet-actionCountForPresentation"}).text
            temp_twitter_dict = {}
            temp_twitter_dict['text'] = text
            temp_twitter_dict['time'] = twitter_time
            temp_twitter_dict['reply'] = reply_num
            temp_twitter_dict['retweet'] = retweet_num
            temp_twitter_dict['favorite'] = favorite_num
            twitter_list.append(temp_twitter_dict)
            db['twitters'].insert(temp_twitter_dict)
        except AttributeError:
            pass
    browser.close()

def gather_price(coinmarketurl):
    data_val = []
    data_head = []
    driver = webdriver.Firefox(executable_path =r'.\geckodriver.exe')
    driver.get(coinmarketurl)
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
    df.to_csv('prices_{}.csv'.format(coinmarketurl.split('/')[-2]))
    driver.close()

def main():
    year = 2015
    month = 1
    day = 1
    days = 732
    date_range = gen_daterange(year, month, day, days)
    word = 'BTC'
    gather_price('https://coinmarketcap.com/currencies/bitcoin/')
    for date in date_range:
        start = str(date)
        end = str(date + timedelta(1))
        scrape_twitter(start, end, word)

if __name__ == '__main__':
    main()