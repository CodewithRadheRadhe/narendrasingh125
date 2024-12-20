# -*- coding: utf-8 -*-
"""Fake_news_classifier_lammet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n2u9qKILhMhds_l0YefU4sb9L_THOOKD
"""

import pandas as pd
import csv

df=pd.read_csv('/content/drive/MyDrive/Files Data science/fake_newsData.csv')

# df = pd.read_csv('/content/fake_newsData.csv', error_bad_lines=False, quoting=pd.QUOTE_ALL)

# try:
#     df = pd.read_csv('/content/fake_newsData.csv',
#                      on_bad_lines='skip', # Skip lines with parsing errors
#                      quoting=csv.QUOTE_NONE, # Disable quoting to handle potential quote issues
#                      escapechar='\\')  # Escape special characters like backslashes
# except pd.errors.ParserError as e:
#     print(f"An error occurred while reading the CSV: {e}")

df

## Get the Independent Features

X=df.drop('label',axis=1)

X.head()

## Get the Dependent features
y=df['label']

y.head()

df.shape
df=df.dropna()
df.head(10)

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

from google.colab import drive
drive.mount('/content/drive')

messages=df.copy()

messages

messages.reset_index(inplace=True)

messages.head(10)

messages['title'][6]

import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['title'][i])
    review = review.lower()
    review = review.split()

    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

corpus[3]

## Applying Countvectorizer
# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,ngram_range=(1,3))
X = cv.fit_transform(corpus).toarray()

# write a function to check accuracy for different train test split size

X.shape
y=messages['label']
## Divide the dataset into Train and Test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)



cv.get_feature_names_out()[:20]

cv.get_params()

df1 = pd.DataFrame(X_train, columns=cv.get_feature_names_out())

df1.columns.value_counts()

df1.shape

df1.head()

import matplotlib.pyplot as plt
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    See full source and example:
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

from sklearn.naive_bayes import MultinomialNB
classifier=MultinomialNB()
from sklearn import metrics
import numpy as np
import itertools
classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)

cm = metrics.confusion_matrix(y_test, pred)
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])

classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
score

y_train.shape

"""**Passive Aggressive Classifier Algorithm**"""

from sklearn.linear_model import PassiveAggressiveClassifier
linear_clf = PassiveAggressiveClassifier(max_iter=50)
linear_clf.fit(X_train, y_train)
pred = linear_clf.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred)
plot_confusion_matrix(cm, classes=['FAKE Data', 'REAL Data'])

"""**Multinomial Classifier with Hyperparameter**"""

classifier=MultinomialNB(alpha=0.1)
previous_score=0
for alpha in np.arange(0,1,0.1):
    sub_classifier=MultinomialNB(alpha=alpha)
    sub_classifier.fit(X_train,y_train)
    y_pred=sub_classifier.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred)
    if score>previous_score:
        classifier=sub_classifier
    print("Alpha: {}, Score : {}".format(alpha,score))

## Get Features names
feature_names = cv.get_feature_names_out()

classifier.feature_log_prob_[0]

# most real
sorted(zip(classifier.feature_log_prob_[0], feature_names), reverse=True)[:20]

### Most fake
sorted(zip(classifier.feature_log_prob_[0], feature_names))[:500]

