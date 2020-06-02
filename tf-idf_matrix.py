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


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect = TfidfVectorizer(analyzer=clean_text)
x_tfidf = tfidf_vect.fit_transform(df['title'])

print(x_tfidf.shape)
print(tfidf_vect.get_feature_names())


final_df = pd.DataFrame(x_tfidf.toarray())
final_df.columns = tfidf_vect.get_feature_names()

print(final_df.head())