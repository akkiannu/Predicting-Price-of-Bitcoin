import spacy
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction import stop_words
from gensim.models.phrases import Phrases, Phraser
from sklearn.base import BaseEstimator, TransformerMixin
from spacy.pipeline import Pipe
nlp = spacy.load('en')

cleaned_tweets = pd.read_json('new_cleaned.json', lines = True)
reviews_token = []
for twitter in cleaned_tweets.text:
    reviews_token.append(twitter.split())



model = Word2Vec(reviews_token, seed = 1, size=200, workers=8, window = 2)
print(len(list(model.wv.vocab.keys())))
model.save("nofilter.w2v")