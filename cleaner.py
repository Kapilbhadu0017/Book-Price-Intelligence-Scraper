import ast
import numpy as np
import pandas as pd

def tonum(s):
    if 'one' in s.lower():
        return '1'
    elif 'two' in s.lower():
        return '2'
    elif 'three' in s.lower():
        return '3'
    elif 'four' in s.lower():
        return '4'
    elif 'five' in s.lower():
        return '5' 
    else:
        return np.nan

df = pd.read_csv('data/raw/books_raw.csv')

# print(df.head())
# print(df.info())

for i in range(len(df['star_rating'])):
    # df['star_rating'][i] = tonum(df['star_rating'][i])
    # print(df['star_rating'][i])
    print(tonum(df['star_rating'][i]))






















# def tonum(s):
#     s = str(s).lower()
#     if s == 'one':
#         return 1
#     elif s == 'two':
#         return 2
#     elif s == 'three':
#         return 3
#     elif s == 'four':
#         return 4
#     elif s == 'five':
#         return 5
#     return np.nan


# def parse_star_rating(value):
#     if isinstance(value, str):
#         value = value.strip()
#         try:
#             parsed = ast.literal_eval(value)
#             if isinstance(parsed, (list, tuple)) and len(parsed) > 1:
#                 return tonum(parsed[1])
#         except (ValueError, SyntaxError):
#             parts = value.split()
#             if len(parts) > 1:
#                 return tonum(parts[-1].strip("[]'\""))
#     return np.nan


# df = pd.read_csv('data/raw/books_raw.csv')

# df = df.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)

# df['price'] = df['price'].str.replace('£', '', regex=False)
# df['price'] = pd.to_numeric(df['price'], errors='coerce')

# df['star_rating'] = df['star_rating'].apply(parse_star_rating)

# df['availability'] = np.where(df['availability'] == 'In stock', 'In stock', 'Out of stock')

# print(df.head())
