import pandas as pd
import re
from langdetect import detect
import json
with open('datagathered_2015_2016.json', 'rb') as f:
    data1 = f.readlines()

with open('data_btc.json', 'rb') as f:
    data2 = f.readlines()
raw_data1 = pd.DataFrame(columns = ['text', 'time','reply','retweet','favorite'])
for row in data1:
    row_dic = json.loads(row)
    raw_data1.loc[-1] = [row_dic['text'], row_dic['time'], row_dic['reply'], row_dic['retweet'], row_dic['favorite']]
    raw_data1.index = raw_data1.index + 1
    raw_data1 = raw_data1.sort_index()
raw_data2 = pd.DataFrame(columns = ['text', 'time','reply','retweet','favorite'])
for row in data2:
    row_dic = json.loads(row)
    raw_data2.loc[-1] = [row_dic['text'], row_dic['time'], row_dic['reply'], row_dic['retweet'], row_dic['favorite']]
    raw_data2.index = raw_data2.index + 1
    raw_data2 = raw_data2.sort_index()

bit_twitter = pd.concat([raw_data1,raw_data2], axis = 0)
bit_twitter = bit_twitter.drop_duplicates()
http = '(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'#delete http
reg_clean2 = '#\w+.\w+.\w+\/\w+|\\n|#\w+|\$\w+|@\w+'#delete # @ ...
reg_clean3 ="\.|’s|#\.?"
reg_clean4 = '\\xa0|[√>\-_]|\/\w+|\b\w+com\b|0x\w+'
def detectlang(string):
    try:
        return detect(string)
    except:
        return 'no feature'
#raw_data = pd.read_json('raw_data.json', lines = True)
def clean(string):
    string = re.sub(http,' ',string)
    string = re.sub(reg_clean2,' ',string)
    string = re.sub(reg_clean3,' ',string)
    string = re.sub(reg_clean4,' ',string)
    a = string.lower().strip().split()
    return " ".join(a)

#raw_data['language'] = raw_data['text'].apply(detectlang)
#eng_twitter = raw_data[raw_data['language'] == 'en']
bit_twitter['text'] = bit_twitter['text'].apply(clean)
with open('bit_cleaned.json', 'w') as f:
    f.write(bit_twitter.to_json(orient='records', lines=True))