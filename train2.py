import tensorflow as tf
import pickle
import csv
from tensorflow import keras
from tensorflow.keras.layers import *

model = keras.Sequential()
epoch = 20
max_len = 900 + 837
vocab = None
#with open('vocab_char.pkl','rb') as f:
with open('vocab_post.pkl','rb') as f:
    vocab = pickle.load(f)
vocab_size = len(vocab.keys())
X = []
Y = []

temp = []
temp2 = []
with open('train.csv','r',encoding='utf-8') as f:
    rd = csv.reader(f)

    for line in rd:
        # print(line)
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
            x.append(vocab[i])
            temp.append(vocab[i])
        for i in x2:
            x.append(vocab[i])
            temp.append(vocab[i])
        X.append(x)

#         temp.append(len(x1))
#         temp2.append(len(x2))
        #print(line[2])
        Y.append(int(line[2]))
        
print(max(temp))
# print(min(temp))
# print(max(temp2))
# print(min(temp2))
# print(tf.constant(X).shape)
# print(tf.constant(Y).shape)

vocab_size = len(vocab.keys())

units = 50 
print(vocab_size)
model.add(
    Embedding(vocab_size,100,input_length=max_len)
)

model.add(
    Bidirectional(LSTM(units))
)

model.add(
    Dense(1,activation='sigmoid')
)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',#'mse',
    metrics=['accuracy']
)

model.summary()

# X_val = X[:10000]
# X = X[10000:]

# Y_val = Y[:10000]
# Y = Y[10000:]

# X_val = tf.constant(X_val)
# Y_val = tf.constant(Y_val)

X = tf.constant(X)
Y = tf.constant(Y)

from tensorflow.keras.callbacks import EarlyStopping

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)

hist = model.fit(X,Y,batch_size=50,epochs=epoch,validation_split=0.1,callbacks=[es])

import matplotlib.pyplot as plt
#print(hist.history.keys())
fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')

acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')
acc_ax.plot(hist.history['val_accuracy'], 'g', label='val acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

model.save('security_bigram')

