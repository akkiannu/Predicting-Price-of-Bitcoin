from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import pandas as pd
import numpy as np
# reference https://www.programmableweb.com/news/how-to-start-using-google-cloud-natural-language-api/how-to/2016/09/01#apiu
data = pd.read_json('new_cleaned.json', lines=True)
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')
data['polarity'] = np.zeros(len(data))
data['magnitude'] = np.zeros(len(data))

def main():

    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])

    http=httplib2.Http()
    credentials.authorize(http)

    service = discovery.build('language', 'v1beta1',
                              http=http, discoveryServiceUrl=DISCOVERY_URL)
    for i in range(len(data)):
        text = data.loc[i,'text']
        service_request = service.documents().analyzeSentiment(
            body={
                'document': {
                    'type': 'PLAIN_TEXT',
                    'content': text
                }
            })

        try:
            response = service_request.execute()
            polarity = response['documentSentiment']['polarity']
            magnitude = response['documentSentiment']['magnitude']
            data.loc[i,'polarity'] = polarity
            data.loc[i,'magnitude'] = magnitude
            print('Sentiment: polarity of %s with magnitude of %s' % (polarity, magnitude))
        except:
            data.loc[i,'polarity'] = None
            data.loc[i,'magnitude'] = None
    with open('twitter_labeled.json', 'w') as f:
        f.write(data.to_json(orient='records', lines=True))
    return 0

if __name__ == '__main__':
    main()