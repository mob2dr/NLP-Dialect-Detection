# -*- coding: utf-8 -*-
"""NLP_project_Data_preprocessing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_z_3PYMX09TaD6CcZf61UCT7F62CpgVE

## Import required libaries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import scipy.sparse
import re
import string
import pyarabic.araby as araby
import nltk
from nltk.corpus import stopwords
import textblob
from textblob import Word
from sklearn import preprocessing

from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer

"""## Define Functions for Pre-processing"""


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def has_diacritics(text):
    arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    stripped_text = araby.strip_diacritics(text)
    stripped_text = araby.strip_shadda(stripped_text)
    stripped_text = araby.strip_tashkeel(stripped_text)
    if stripped_text != text:
      return 1
    else :
      return 0

def remove_diacritics(text):
    arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(arabic_diacritics, '', text)
    text = araby.strip_diacritics(text)
    text = araby.strip_shadda(text)
    text = araby.strip_tashkeel(text)
    return text


"""The presence of Latin characters will mess with transliteration later on.

so, we should remove them.
also, remove linsk (https), Hashtages and digits.
"""


def remove_non_arabic(text):
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)
    text = re.sub('([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', ' ', text)
    text = re.sub(r'\\u[A-Za-z0-9\\]+', ' ', text)
    return text


def remove_repeating_characters(text):
    text = text.strip()
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    # text = re.sub(r'(.)\1+', r'\1', text)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    return text


"""## Text Pre-processing

- **Removing Punctuations and Symbols**
"""

english_punctuations = string.punctuation
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
punctuations_list = arabic_punctuations + english_punctuations
nltk.download('stopwords')
stop = stopwords.words('arabic')
nltk.download('wordnet')


def clean_data(data):
    data['text'] = data['text'].apply(remove_punctuations)

    """- **Remove Emojis**"""

    data['text'] = data['text'].apply(remove_emoji)

    """- **Stop Words Elimination**"""

    #data['text'] = data['text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    data['has_diacritics'] = data['text'].apply(has_diacritics)
    """- **Remove Diacritics**"""

    data['text'] = data['text'].apply(remove_diacritics)

    """- **Remove Non-Arabic Characters**"""

    data['text'] = data['text'].apply(remove_non_arabic)

    """- **Remove Repeated Characters**"""

    data['text'] = data['text'].apply(remove_repeating_characters)

    """- **Lemmatisation**"""

    data['text'] = data['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    """- **Encoding the Target Classes**"""

    # Create a dictionary to map the labels to their encoded values
    label_map = {'EG': 0, 'LY': 2, 'LB': 1, 'SD': 4, 'MA': 3}

    # Create a new column with the encoded labels
    data['dialect'] = data['dialect'].map(label_map)
    data.dropna()
    data = data.sample(frac=1)
    return data


def clean_text(text):
    text = remove_punctuations(text)

    """- **Remove Emojis**"""

    text = remove_emoji(text)

    """- **Stop Words Elimination**"""

    #text = " ".join(x for x in text.split() if x not in stop)

    """- **Remove Diacritics**"""

    text = remove_diacritics(text)

    """- **Remove Non-Arabic Characters**"""

    text = remove_non_arabic(text)

    """- **Remove Repeated Characters**"""

    text = remove_repeating_characters(text)

    """- **Lemmatisation**"""
    text = " ".join([Word(word).lemmatize() for word in text.split()])

    return text


def preprocess(data=None, text=None):
    return clean_data(data) if data is not None else clean_text(text)

