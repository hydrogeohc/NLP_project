# -*- coding: utf-8 -*-

####
#### NLP projects
### import library ###
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import tensorflow
from tensorflow import keras
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense,Embedding,Dropout,LSTM
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

#### read data ###

data=pd.read_csv("Corona_NLP_test.csv")
data['Sentiment']=LabelEncoder().fit_transform(data['Sentiment'])
data=data.dropna(axis=1)
data.head()

x=data.drop('Sentiment',axis=1)
y=data['Sentiment'].values
y=y.reshape(-1,1)

nltk.download('stopwords')
message=x.copy()
message.reset_index(inplace=True)

ps=PorterStemmer()
corpus=[]
for i in range(len(x)):
  review=re.sub('[^a-zA-Z]',' ',message['OriginalTweet'][i])
  review=review.lower()
  review=review.split()
  review=[ps.stem(word) for word in review if not word in stopwords.words('english')]
  review=' '.join(review)
  corpus.append(review)

voc_size=50000
one_hot_r=[one_hot(word,voc_size) for word in corpus]

sent_length=30
input=pad_sequences(one_hot_r,padding='pre',maxlen=sent_length)

final_input=np.array(input)
final_output=np.array(y)

x_train, x_test, y_train, y_test = train_test_split(final_input,final_output, test_size=0.33, random_state=42)
x_train.shape

dim=40
model=Sequential()
model.add(Embedding(voc_size,dim,input_length=sent_length))
model.add(Dropout(0.3))
model.add(LSTM(80))
model.add(Dropout(0.3))
model.add(Dense(1,activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train,y_train,batch_size=50,epochs=120,validation_data=(x_test,y_test))

y_pred=model.predict_classes(x_test)

val=metrics.accuracy_score(y_test,y_pred)
print("accuracy is =",str(val*100)+" %")













