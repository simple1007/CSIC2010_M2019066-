from tensorflow import keras
import csv
import pickle

max_len = 900 + 837
vocab = None
with open('vocab_char.pkl','rb') as f:
    vocab = pickle.load(f)
X = []
Y = []

model = keras.models.load_model("security")

with open('test.csv','r',encoding='utf-8') as f:
    rd = csv.reader(f)

    for line in rd:
        x1 = list(line[0]) + ['<PAD>'] * (900 - len(line[0]))
        x2 = list(line[1]) + ['<PAD>'] * (837 - len(line[1])) 
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

print('evaluate')
result = model.evaluate(X, Y)
print(result)
print('---------')
print('f1-score')
result = model.predict(X)
# print(Y)
from sklearn.metrics import f1_score
# print(result)
y_pred = []
for index,re in enumerate(result):
    re_ = re[0]
    y_pred.append(round(re_))
print(f1_score(Y, y_pred))

