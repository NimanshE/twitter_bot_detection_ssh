import pandas as pd
import numpy as np

from scraper import Profile

from flask import Flask, request
from flask_cors import CORS
from sklearn import tree


clf = None  # Initialize the model


def load_and_train_model():
    global clf
    train_data = pd.read_csv('Model/kaggle_train.csv')
    train_attr = train_data[['followers_count', 'friends_count', 'statuses_count', 'verified']]
    train_label = train_data[['bot']]

    clf = tree.DecisionTreeClassifier()
    X = train_attr.values
    Y = train_label.values
    clf = clf.fit(X, Y)


app = Flask(__name__)
CORS(app)


@app.get("/")
def main_func():

    if clf is None:
        load_and_train_model()

    currProfile = Profile(request.args.to_dict()["id"])
    user_data = np.array([[
        currProfile.followers,
        currProfile.following,
        currProfile.num_tweets,
        currProfile.verified
    ]])

    predicted = clf.predict(user_data)
    result = {
        "pred": predicted.item(0)
    }
    return result


if __name__ == "__main__":
    app.run()
