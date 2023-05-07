# -*- coding: utf-8 -*-
"""SVC_MODEL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kSR-0aK1uFwHBu_aujyCCf1nF6oKwS43
"""

import pandas as pd 
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import pickle

def dialect_predict(model_path,sentence):
  model = pickle.load(open(model_path,"rb"))
  sentence =[sentence]
  dialect = model.predict(sentence)

  if dialect == 0:
    country = "Egypt"

  elif  dialect == 1 :
    country = "Lebnanon"

  elif dialect ==   2 :
    country = "Libya"

  elif dialect == 3:
    country = "Morocco"

  else:
    country = "Sudan"
  
  return country
