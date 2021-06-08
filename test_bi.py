from tensorflow import keras
import csv
import pickle

max_len = 900 + 837
vocab = None
with open('vocab_post.pkl','rb') as f:
    vocab = pickle.load(f)
X = []
Y = []

model = keras.models.load_model("security_bigram")

with open('test.csv','r',encoding='utf-8') as f:
    rd = csv.reader(f)

    for line in rd:
        x1 = []
        x2 = []

        for i in range(len(line[0])-1):
            x1.append(line[0][i:i+2])
        for i in range(len(line[1])-1):
            x2.append(line[1][i:i+2])

            
        x1 = x1 + ['<PAD>'] * (900 - len(x1))
        x2 = x2 + ['<PAD>'] * (837 - len(x2)) 
        x = []
        
        for i in x1:
            if i in vocab:
                x.append(vocab[i])
            else:
                x.append(vocab['<UNK>'])
        for i in x2:
            if i in vocab:
                x.append(vocab[i])
            else:
                x.append(vocab['<UNK>'])
        X.append(x)

        Y.append(int(line[2]))

import math
import tensorflow as tf
from sklearn.metrics import f1_score

result = model.evaluate(X, Y)
print('evaluate')
print(result)
print('---------')
print('f1-score')
result = model.predict(X)

y_pred = []
for i in result:
    i = round(i[0])
    y_pred.append(i)

print(f1_score(Y, y_pred))
