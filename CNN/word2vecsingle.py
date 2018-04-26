import spacy
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction import stop_words
from gensim.models.phrases import Phrases, Phraser
from sklearn.base import BaseEstimator, TransformerMixin
from spacy.pipeline import Pipe
nlp = spacy.load('en')

common_terms = list(stop_words.ENGLISH_STOP_WORDS) + ["'m", "'re", "'ll", "'s", "'ve", "'d", 'ca', 'is']

common_terms.remove('not')
common_terms.remove('nothing')
common_terms.remove('never')
cleaned_tweets = pd.read_json('new_cleaned.json', lines = True)
class getsingleword(BaseEstimator, TransformerMixin):
    def __init__(self,  stop_words=None):

        self.stop_words = stop_words

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        preprocessed_sentences = []

        for doc in nlp.pipe(X, n_threads=8):
            if self.stop_words is not None:
                preprocessed_sentences.append([t.lower_ for t in doc if not t.is_punct and t.lemma_ not in self.stop_words])
            else:
                preprocessed_sentences.append([t.lower_ for t in doc if not t.is_punct])


        return preprocessed_sentences

gsl = getsingleword(stop_words=common_terms)
reviews_token = gsl.fit_transform(cleaned_tweets.text)
model = Word2Vec(reviews_token, seed = 1,min_count = 5, size=100, workers=8, window = 3)
model.save("singleword2v.w2v")