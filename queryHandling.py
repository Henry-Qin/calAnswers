__author__ = 'henryqin'

import sys
import pandas as pd
# import nltk
from nltk import pos_tag
from nltk import word_tokenize
from difflib import get_close_matches


#example query: departments with an avg_age of 50
# nltk.download('averaged_perceptron_tagger')


df = pd.read_excel('Sample_data.xlsx', sheetname='Sheet1')
columnNames = list(df)

countKeyWords = ['how many', 'number']
countKeyWordsSet = set(countKeyWords)

while(1):
    print('Enter Query:')
    inputStr = sys.stdin.readline()
    text = word_tokenize(inputStr)
    posText = pos_tag(text)
    nouns = [word[0] for word in posText if word[1][0] == "N"]
    numbers = [word[0] for word in posText if word[1] == "CD"]
    comparatives = [word[0] for word in posText if word[1] == "JJR"]
    superlatives = [word[0] for word in posText if word[1] == "JJS"]
    columnsSelected = [get_close_matches(n, columnNames, cutoff=0.3)[0] for n in nouns]
    print(df[columnsSelected])
