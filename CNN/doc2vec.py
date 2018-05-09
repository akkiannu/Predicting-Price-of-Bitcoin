import gensim
import pandas as pd
import io
import sys
from collections import namedtuple
from gensim.models.doc2vec import TaggedDocument
import random
from random import shuffle
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
lot_review = pd.read_json('final_twitter.json', lines=True)

all_text = list(lot_review.text)
'''docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for i, text in enumerate(all_text):
    words = text.lower().split()
    tags = [i]
    docs.append(analyzedDocument(words, tags))

model = gensim.models.Doc2Vec(docs, size=200, min_count=5, workers=8, window = 300)'''

docs=[TaggedDocument(all_text[i], [str(i)]) for i in range(len(all_text)) ]
model = gensim.models.Doc2Vec(size=200, window=5, min_count=5, workers=11)
model.build_vocab(docs)
for epoch in range(20):
    shuffle(docs)
    # in each epoch, all samples are used
    model.train(docs, total_examples=len(docs), epochs=1)

'''model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025)

model.build_vocab(docs)

for epoch in range(10):
    model.train(docs, total_examples=model.corpus_count,epochs=10)
    model.alpha -= 0.002            # decrease the learning rate
    model.min_alpha = model.alpha       # fix the learning rate, no deca
    model.train(docs)'''

model.save('doc2vec.w2v')