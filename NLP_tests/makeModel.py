from keras.layers import Dense, Dropout, Activation
from keras.models import Sequential
import json
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer
import numpy as np
import string

training = np.genfromtxt('./tennis5.csv', delimiter='|', dtype=None)

train_x = [x[1].decode(errors="ignore") for x in training]
train_y = np.asarray([x[0] for x in training])

max_words = 4000
# printable = set(string.printable)
# printable.add("|")

tokenizer = Tokenizer(num_words=max_words, lower=True, split=" ")

# str1 = " ".join(str(x) for x in train_x)
# filter(lambda x: x in printable, s)
# print(len(str1))
# with open("zz2.txt", "w") as file1:
# file1.write(str1)
tokenizer.fit_on_texts(train_x)
# print(tokenizer.word_index)
# print(tokenizer.word_counts)
# print(tokenizer.document_count)
# print(tokenizer.word_index)
# print(tokenizer.word_docs)
dictionary = tokenizer.word_index
with open('dictionary.json', 'w') as dictionary_file:
    json.dump(dictionary, dictionary_file)


def convert_text_to_index_array(text):
    return [dictionary.get(word) for word in kpt.text_to_word_sequence(text) if dictionary.get(word) is not None]


allWordIndices = []
for text in train_x:
    wordIndices = convert_text_to_index_array(str(text))
    allWordIndices.append(wordIndices)

allWordIndices = np.asarray(allWordIndices)

train_x = tokenizer.sequences_to_matrix(allWordIndices, mode='binary')
train_y = keras.utils.to_categorical(train_y, 2)


model = Sequential()
model.add(Dense(512, input_shape=(max_words,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='cosine_proximity',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(train_x, train_y,
          batch_size=32,
          epochs=5,
          verbose=1,
          validation_split=0.1,
          shuffle=True)

model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights('model.h5')

print('saved model!')
