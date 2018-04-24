from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pandas as pd
import numpy as np

#instantiates a client
client = language.LanguageServiceClient()
data = pd.read_json('new_cleaned.json', lines=True)
data['polarity'] = np.zeros(len(data))

data['score'] = np.zeros(len(data))
#The text to analyze
def main():
    count = 0
    for i in range(len(data)):
        text = data.loc[i,'text']

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

    #Detects the sentiment of the text
        try:
            sentiment = client.analyze_sentiment(document=document,
                                                 encoding_type='UTF32').document_sentiment
            data.loc[i,'score'] = sentiment.score
            data.loc[i,'magnitude'] = sentiment.magnitude
            print('Text: {}'.format(text))
            print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
            count += 1
            print(count)

        except:
            data.loc[i,'score'] = None
            data.loc[i,'magnitude'] = None
    with open('twitter_labeled_v2.json', 'w') as f:
        f.write(data.to_json(orient='records', lines=True))
    return 0




if __name__ == '__main__':
    main()

