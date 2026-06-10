import ast
import numpy as np
import pandas as pd

def tonum(s):
    s = str(s).lower()
    if 'one' in s:
        return 1
    elif 'two' in s:
        return 2
    elif 'three' in s:
        return 3
    elif 'four' in s:
        return 4
    elif 'five' in s:
        return 5 
    else:
        return np.nan

df = pd.read_csv('data/raw/books_raw.csv')

df['price'] = pd.to_numeric(df['price'].str.replace('£','', regex=False), errors='coerce')

df['star_rating'] = df['star_rating'].apply(tonum)

df[['title','category','availability']] = df[['title','category','availability']].apply(lambda c: c.str.strip())

df['availability'] = np.where(df['availability'].str.contains('In stock', na=False), 'In stock', 'Out of stock')

df = df.drop_duplicates()

df.to_csv('data/clean/books_clean.csv', index = False)
print("Data Cleaned Successfully, saved at: 'data/clean/books_clean.csv'")
