import nltk
import pandas as pd

# nltk.download()
pd.set_option('display.max_colwidth', 100)

df = pd.read_csv('data/reddit_data.csv')

print(df.head())

print(df.shape)

# Getting Description
print(df['num_comments'].describe())

print('Num of null in label: {}'.format(df['num_comments'].isnull().sum()))

##REMOVE PUNCTUATION
import string

print(string.punctuation)


def remove_punc(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    return text_nopunct


##EACH ROW OF TITLE

''' python is case sensetive for that A and a is diffrent thats why lower()'''
df['title_clean'] = df['title'].apply(lambda x: remove_punc(x.lower()))
print(df.head())

# TOKENIZATION
import re


def tokenize(text):
    # Split word non word
    tokens = re.split('\W+', text)
    return tokens
##EACH ROW OF TITLE
df['title_tokenize'] = df['title_clean'].apply(lambda x: tokenize(x))
print(df.head())

##Remove stopwords (does not contribute much in sentence)
stopword = nltk.corpus.stopwords.words('english')


def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]
    return text

df['title_nostopwords'] = df['title_tokenize'].apply(lambda x: remove_stopwords(x))
print(df.head())



def clean_text(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    tokens = re.split('\W+', text_nopunct)
    text = [word for word in tokens if word not in stopword]
    return text

''' python is case sensetive for that A and a is diffrent thats why lower()'''
df['title_final_clean'] = df['title'].apply(lambda x: clean_text(x.lower()))
print(df.head())


##Stemming
ps = nltk.PorterStemmer()
def stemming(tokenized_text):
    text = [ps.stem(word) for word in tokenized_text]
    return text

df['title_stem'] = df['title_final_clean'].apply(lambda x: stemming(x))
print(df.head())


##Lemmatizing
wn = nltk.WordNetLemmatizer()

'''
print(ps.stem('meanness'))
print(ps.stem('meaning'))


print(wn.lemmatize('meanness'))
print(wn.lemmatize('meaning'))



print(ps.stem('goose'))
print(ps.stem('geese'))


print(wn.lemmatize('goose'))
print(wn.lemmatize('geese'))
'''

def lemmatizing(tokenized_text):
    text = [wn.lemmatize(word) for word in tokenized_text]
    return text

''' not used stem dataset'''
#lemmatization more accurate
df['title_lemma'] = df['title_final_clean'].apply(lambda x: lemmatizing(x))
print(df.head())
