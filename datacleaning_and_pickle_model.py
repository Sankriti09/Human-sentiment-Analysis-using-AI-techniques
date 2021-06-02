import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

#read csv file consist of dataset
df = pd.read_csv('Balanced_reviews.csv')
#starting investigations
df.shape
df.ndim
df.head()

#dropping null values
df.dropna(inplace=True)
df.shape

#start categorizing reviews, less than 3 rating stores value '1' else '0' in new column 'Positivity'
df = df[df['overall']!=3]


df.shape
df['reviewText'].head()
df.iloc[0,1]
df['reviewText'].value_counts()

#train-test split
features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'], random_state = 42)    

#using TF-IDF Vectorizer to convert text data into numeric
vect = TfidfVectorizer(min_df=5).fit(features_train)
features_train_vectorized = vect.transform(features_train)

vect.vocabulary_

#applying Logistic Regression for the model
model = LogisticRegression()

#fitting data
model.fit(features_train_vectorized, labels_train)
predictions = model.predict(vect.transform(features_test))

#roc score checks the performance and quality of our model
roc_auc_score(labels_test, predictions)

pkl_filename = "pickle_model.pkl"
vocab_filename = "vocab_model.pkl"

#dumping model to pickle file
with open(pkl_filename,'wb') as file:
    pickle.dump(model, file)

#ship pickle file to client(client use and handle), moreover saving pickle file for future use
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)

#save the TF-IDF Vocabulary
pickle.dump(vect.vocabulary_, open(vocab_filename,'wb'))