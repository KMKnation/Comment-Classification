import nltk
import pandas as pd
wn = nltk.WordNetLemmatizer()

# nltk.download()
pd.set_option('display.max_colwidth', 100)

df = pd.read_csv('data/reddit_data.csv')

import re
import string
stopword = nltk.corpus.stopwords.words('english')


def clean_text(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    tokens = re.split('\W+', text_nopunct)
    text = [word for word in tokens if word not in stopword]
    return text

''' python is case sensetive for that A and a is diffrent thats why lower()'''
df['title_final'] = df['title'].apply(lambda x: clean_text(x.lower()))


def lemmatizing(tokenized_text):
    text = [wn.lemmatize(word) for word in tokenized_text]
    return text

df['title_final'] = df['title_final'].apply(lambda x: lemmatizing(x))
print(df.head())

#Vectorizing


from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(analyzer=clean_text)
X_counts = count_vect.fit_transform(df['title_final'])

#1253 uniq words and 1846 rows
print(X_counts.shape)
print(count_vect.get_feature_names())

data_sample = df[0:20]

count_vect_sample = CountVectorizer(analyzer=clean_text)
X_counts_sample = count_vect_sample.fit_transform(data_sample['title_final'])
print(X_counts_sample.shape)
print(count_vect_sample.get_feature_names())

print(X_counts_sample)

##Vectorizing output sparse matrix
X_counts_df = pd.DataFrame(X_counts_sample.toarray())

print(X_counts_df)


##TOGET NAMES
X_counts_df.columns = count_vect_sample.get_feature_names()
print(X_counts_df)




'''

VECTORIZING RAW Data: N-GRAMS

'''