import pandas as pd
import re
from langdetect import detect


http = '(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'#delete http
reg_clean2 = '#\w+.\w+.\w+\/\w+|\\n|#\w+|\$\w+|@\w+'#delete # @ ...
reg_clean3 ="\.|’s|#\.?"
reg_clean4 = '\\xa0|[√>\-_]|\/\w+|\b\w+com\b|0x\w+'
def detectlang(string):
    try:
        return detect(string)
    except:
        return 'no feature'
raw_data = pd.read_json('raw_data.json', lines = True)
def clean(string):
    string = re.sub(http,' ',string)
    string = re.sub(reg_clean2,' ',string)
    string = re.sub(reg_clean3,' ',string)
    string = re.sub(reg_clean4,' ',string)
    a = string.lower().strip().split()
    return " ".join(a)

raw_data['language'] = raw_data['text'].apply(detectlang)
eng_twitter = raw_data[raw_data['language'] == 'en']
eng_twitter['text'] = eng_twitter['text'].apply(clean)
with open('new_cleaned.json', 'w') as f:
    f.write(eng_twitter.to_json(orient='records', lines=True))