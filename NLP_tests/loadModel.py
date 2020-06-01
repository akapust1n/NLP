
import numpy as np
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
import json
import csv
import warnings

warnings.filterwarnings('ignore')
tokenizer = Tokenizer(num_words=4000)
labels = ['negative', 'positive']

with open('dictionary.json', 'r') as dictionary_file:
    dictionary = json.load(dictionary_file)


def convert_text_to_index_array(text):
    words = kpt.text_to_word_sequence(text)
    wordIndices = []
    for word in words:
        if word in dictionary:
            wordIndices.append(dictionary[word])
        else:
            print("'%s' not in training corpus; ignoring." % (word))
    return wordIndices


json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

model.load_weights('model.h5')

infile = open('testTennis.csv', 'r')
csvReader = csv.reader(infile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
for row in csvReader:
   # print(row)
    evalSentence = row[1]
    testArr = convert_text_to_index_array(evalSentence)
    input = tokenizer.sequences_to_matrix([testArr], mode='binary')
    pred = model.predict(input)
    print("%s sentiment; %f%% confidence" %
          (labels[np.argmax(pred)], pred[0][np.argmax(pred)] * 100))
