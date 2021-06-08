import tensorflow as tf
import pickle
import csv
from tensorflow import keras
from tensorflow.keras.layers import *

model = keras.Sequential()
epoch = 20
max_len = 900 + 837
vocab = None
with open('vocab_char.pkl','rb') as f:
    vocab = pickle.load(f)
vocab_size = len(vocab.keys())
X = []
Y = []

with open('train.csv','r',encoding='utf-8') as f:
    rd = csv.reader(f)

    for line in rd:
        # print(line)
        x1 = list(line[0]) + ['<PAD>'] * (900 - len(line[0]))
        x2 = list(line[1]) + ['<PAD>'] * (837 - len(line[1])) 
        x = []
        for i in x1:
            x.append(vocab[i])
        for i in x2:
            x.append(vocab[i])
        X.append(x)
        
        #print(line[2])
        Y.append(int(line[2]))
print(tf.constant(Y).shape)
vocab_size = len(vocab.keys())

units = 50 

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

model.save('security')
