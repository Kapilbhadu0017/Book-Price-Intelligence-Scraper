import sqlite3
import pandas as pd

df = pd.read_csv('data/clean/books_clean.csv')

conn = sqlite3.connect('data/books.db')

df.to_sql('books', conn, if_exists='replace', index=False)

cursor = conn.cursor()
cursor.execute('select count(*) from books')

print('Total rows:', cursor.fetchone()[0])

conn.close()
print("Table 'books' ready in Database at 'data/books.db'")