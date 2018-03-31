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
from config import *
import pymongo
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
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
            db[MONGO_TABLE].insert(temp_twitter_dict)
        except AttributeError:
            pass
    browser.close()
def main():
    year = 2017
    month = 2
    day = 1
    days = 364
    date_range = gen_daterange(year, month, day, days)
    word = 'XVG'
    for date in date_range:
        start = str(date)
        end = str(date + timedelta(1))
        scrape_twitter(start, end, word)

if __name__ == '__main__':
    main()