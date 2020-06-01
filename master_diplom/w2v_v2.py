import gensim
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from gensim.models.word2vec import Word2Vec
from sklearn.preprocessing import scale
from sklearn.calibration import CalibratedClassifierCV

import numpy as np
import os
import random
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

data_path = "data/"
pos_files = os.listdir(data_path + "pos/")
neg_files = os.listdir(data_path + "neg/")

# for pos_file in pos_files:
#   with open(data_path + "pos/" + pos_file, 'r') as infile:
#      each = ''
#     each_article = infile.readlines()
#    for each_sentence in each_article:
#       each += each_sentence
#  pos_reviews += each
# for neg_file in neg_files:
#   with open(data_path + "neg/" + neg_file, 'r') as infile:
#      each = ''
#     each_article = infile.readlines()
#    for each_sentence in each_article:
#       each += each_sentence
#  neg_reviews += each

for pos_file in pos_files:  # only for 1 file
    with open(data_path + "pos/" + pos_file, 'r') as infile:
        pos_reviews = infile.readlines()

for neg_file in neg_files:
    with open(data_path + "neg/" + neg_file, 'r') as infile:
        neg_reviews = infile.readlines()
    # use 1 for positive sentiment, 0 for negative

y = np.concatenate((np.ones(len(pos_reviews)), np.zeros(len(neg_reviews))))

x_train, x_test, y_train, y_test = train_test_split(
    np.concatenate((pos_reviews, neg_reviews)), y, test_size=0.2)


# Do some very minor text preprocessing
def cleanText(corpus):
    punctuation = """.,?!:;(){}[]"""
    corpus = [z.lower().replace('\n', '') for z in corpus]
    corpus = [z.replace('<br />', ' ') for z in corpus]

    # treat punctuation as individual words
    for c in punctuation:
        corpus = [z.replace(c, ' %s ' % c) for z in corpus]
    corpus = [z.split() for z in corpus]
    return corpus


x_train = cleanText(x_train)
x_test = cleanText(x_test)

n_dim = 300
# Initialize model and build vocab
imdb_w2v = Word2Vec(size=n_dim, min_count=10)
imdb_w2v.build_vocab(x_train)

# Train the model over train_reviews (this may take several minutes)
imdb_w2v.train(x_train, total_examples=imdb_w2v.corpus_count,
               epochs=imdb_w2v.iter)


# Build word vector for training set by using the average value of all word vectors in the tweet, then scale
def buildWordVector(text, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in text:
        try:
            vec += imdb_w2v[word].reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec


train_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_train])
train_vecs = scale(train_vecs)

# Train word2vec on test tweets
imdb_w2v.train(x_test, total_examples=imdb_w2v.corpus_count,
               epochs=imdb_w2v.iter)

test_vecs = np.concatenate([buildWordVector(z, n_dim) for z in x_test])
test_vecs = scale(test_vecs)

lr = CalibratedClassifierCV()
lr.fit(train_vecs, y_train)

print('Test Accuracy: %.2f' % lr.score(test_vecs, y_test))
print(lr.predict_proba([test_vecs[0]]))
print(len(test_vecs))
pred_probas = lr.predict_proba(test_vecs)[:, 1]

fpr, tpr, _ = roc_curve(y_test, pred_probas)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='area = %.2f' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.legend(loc='lower right')
plt.show()
