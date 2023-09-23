import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn import tree, metrics

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

import matplotlib.pyplot as plt
import random

train_data = pd.read_csv('kaggle_train.csv')

bot_data = pd.read_csv('bots_data.csv',encoding='latin-1')
nonbot_data = pd.read_csv('nonbots_data.csv')
test_data = pd.read_csv('test.csv')

train_attr = train_data[['followers_count', 'friends_count', 'statuses_count', 'verified']]
train_label = train_data[['bot']]

bot_attr = bot_data[['followers_count', 'friends_count','statuses_count', 'verified']]
bot_label = bot_data[['bot']]

nonbot_attr = nonbot_data[ ['followers_count', 'friends_count','statuses_count', 'verified']]
nonbot_label = nonbot_data[['bot']]

test_attr = test_data[['followers_count', 'friends_count','statuses_count', 'verified']]
test_label = test_data[['bot']]

clf = tree.DecisionTreeClassifier()

X = train_attr.values
Y = train_label.values
clf = clf.fit(X, Y)

# Testing on Test data

actual = np.array(test_label)
predicted = clf.predict(test_attr)
pred = np.array(predicted)

accuracy = accuracy_score(actual, pred) * 100
precision = precision_score(actual, pred) * 100
recall = recall_score(actual, pred) * 100
f1 = f1_score(actual, pred)
auc = roc_auc_score(actual, pred)

print(f'Accuracy is {accuracy:.4f}%')
print(f'Precision is {precision:.4f}%')
print(f'Recall is {recall:.4f}%')
print(f'F1 Score is {f1:.4f}')
print(f'Area Under Curve is {auc:.4f}')

train_data = pd.read_csv('kaggle_train.csv')
train_label = train_data[['bot']]
test_data = pd.read_csv('test.csv')
test_label = test_data[['bot']]

# Improving the Model

train_X, test_X, train_Y, test_Y = train_test_split(train_data, train_label, test_size=0.4, random_state=0)

X = train_X[['followers_count', 'friends_count','statuses_count', 'verified']].values
Y = train_Y.values
clf = tree.DecisionTreeClassifier()

clf = clf.fit(X, Y)

Z = test_X[['followers_count', 'friends_count','statuses_count', 'verified']].values
actual = np.array(test_Y)
predicted = clf.predict(Z)
pred = np.array(predicted)

sc = test_X['screen_name'].values
i = 0
for name in sc:
    if 'bot' in name or 'Bot' in name or 'bOt' in name or 'boT' in name or 'BOT' in name or 'BOt' in name or 'BoT' in name or 'bOT' in name:
        pred[i] = 1
    i += 1

print("\nBot Values in the test data:")
print(pred)

sample_data = pd.read_csv('sample_data.csv')

sample_Z = sample_data[['followers_count', 'friends_count','statuses_count', 'verified']].values
sample_predict = clf.predict(sample_Z)
fin_pred = np.array(sample_predict)

sc = sample_data['screen_name'].values
i = 0
for name in sc:
    if 'bot' in name or 'Bot' in name or 'bOt' in name or 'boT' in name or 'BOT' in name or 'BOt' in name or 'BoT' in name or 'bOT' in name:
        pred[i] = 1
    i += 1

print("\nBot Values in the sample data:")
print(fin_pred)