import pandas as pd
import numpy as np
import fnmatch
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.pyplot import imshow
import matplotlib

from skimage import color
from skimage import io

import random

# Helper functions for database formatting
def repl(string):
    string1 = string.replace(']','').replace('[', '').replace('\'','')
    return string1

def str_to_list(string):
    lst = list(string[1:-1].split(", "))
    lst1 = []
    for el in lst:
        lst1.append(el[1:-1])
    lst1 = list(set(lst1))
    lst2 =[]
    for el in lst1:
        lst2.append(space_to_underscore(el))
    
    return ' '.join(lst2)

def one_decimal(rating):
    return round(rating, 1)

def categorize_ratings(df, col):
    df[col] = df[col].apply(one_decimal)
    return df
def lower(text):
    return text.lower()

def lower_cols(df, cols):
    for col in cols:
        df[col] = df[col].apply(lower)
    return df

def remove_spaces(text):
    text = text.replace(' ', '', 10)
    return text

def space_to_underscore(text):
    text = text.replace(' ', '_',10)
    return text

def join_names(df, col):
    df[col] = df[col].apply(remove_spaces)
    return df

def read_books_info(filespath='../data/big_data_temp/'):
    pattern = 'gr_books_df_*.csv'
    print('Pattern :', pattern )

    files = os.listdir(filespath) 
    dfs_files = []
    for name in files: 
        if fnmatch.fnmatch(name, pattern):
            dfs_files.append(name)
    dfs_files
    dfs_paths = []
    for file in dfs_files:
        dfs_paths.append(filespath + file)

    revs_lst = []
    for file in dfs_paths:
        try:
            revs_lst.append(pd.read_csv(file))
        except:
            print(f'file {file} failed')
    print(len(revs_lst))
    df = pd.concat(revs_lst,axis=0)
    return df

def add_space(text):
    return text + " "

def repl(string):
    string1 = string.replace(']','').replace('[', '').replace('\'','')
    return string1

def str_to_list(string):
    lst = list(string[1:-1].split(", "))
    lst1 = []
    for el in lst:
        lst1.append(el[1:-1])
    lst1 = list(set(lst1))
    lst2 =[]
    for el in lst1:
        lst2.append(space_to_underscore(el))
    
    return ' '.join(lst2)

def one_decimal(rating):
    return round(rating, 1)

def categorize_ratings(df, col):
    df[col] = df[col].apply(one_decimal)
    return df
def lower(text):
    return text.lower()

def lower_cols(df, cols):
    for col in cols:
        df[col] = df[col].apply(lower)
    return df

def remove_spaces(text):
    text = text.replace(' ', '', 10)
    return text

def space_to_underscore(text):
    text = text.replace(' ', '_',10)
    return text

def join_names(df, col):
    df[col] = df[col].apply(remove_spaces)
    return df

def read_books_info(filespath='../data/big_data_temp/'):
    '''
    Imports the dataframe from files and does preliminary cleaning.
    
    Input:
    ------
    filepath : str
                directory where files live.
    
    Return:
    -------
    df : pd.DataFrame
                Pandas dataframe containing all content information
    '''
    pattern = 'gr_books_df_*.csv'
    print('Pattern :', pattern )

    files = os.listdir(filespath) 
    dfs_files = []
    for name in files: 
        if fnmatch.fnmatch(name, pattern):
            dfs_files.append(name)
    dfs_files
    dfs_paths = []
    for file in dfs_files:
        dfs_paths.append(filespath + file)

    revs_lst = []
    for file in dfs_paths:
        try:
            revs_lst.append(pd.read_csv(file))
        except:
            print(f'file {file} failed')
    print(len(revs_lst))
    df = pd.concat(revs_lst,axis=0)
    return df

def clean_books_df(filepath):
    '''
    Returnes a clean dataframe by extracting and cleaning data from the files 
    that lives in filepath
    
    Input:
    ------
    filepath : str
    Return:
    -------
    books_df : pd.DataFrame
    '''
    books_df = read_books_info(filepath)
    books_df['author_name'] = books_df['author_name'].apply(repl)
    # books_df = categorize_ratings(books_df,'avg_rating')
    books_df['genres'] = books_df['genres'].apply(str_to_list)
    books_df = books_df[['isbn', 'book_title', 'avg_rating', 'author_name', 'book_desc', 'genres']]
    books_df = lower_cols(books_df, ['book_title', 'author_name', 'book_desc', 'genres'])
    books_df = join_names(books_df, 'author_name')
    books_df.reset_index(inplace=True)
    books_df['genres'] = books_df['genres'].apply(add_space)
    return books_df

# TfIdf
def display_scores(vectorizer, tfidf_result):
    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=1)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
#     for item in sorted_scores:
#         print('{0:50} Score: {1}'.format(item[0], item[1]))
    return sorted_scores

def transform_format(val):
    if val == 255:
        return 255
    else:
        return val

def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def brown_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 21.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def green_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 80.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def blue_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 130.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def purple_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 160.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def fuksi_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 220.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def red_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 250.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def yellow_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 40.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)

def check(string, word):
    if word in string:
        return True
    else:
        return False
    
def display_scores_wc(word_nums, words):
    scores = zip(words, word_nums)
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
#     for item in sorted_scores:
#         print('{0:50} Score: {1}'.format(item[0], item[1]))
    return sorted_scores

def get_rid_of_words(text):
    words_to_remove = [' audiobook ', ' science ', ' popular_science ', ' nonfiction ']
    for word in words_to_remove:
        text = text.replace(word, ' ', 500)
    return text

