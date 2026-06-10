import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('data/books.db')

# Query 1 — average price by category, ordered descending → horizontal bar chart
q1 = pd.read_sql_query("""
                    SELECT category, ROUND(AVG(price), 2) as avg_price
                        FROM books
                       GROUP BY category
                       ORDER BY avg_price DESC
""",conn)

# Query 2 — top 10 most expensive books → horizontal bar chart
q2 = pd.read_sql_query("""
                       SELECT title, price, category
                       FROM books
                       ORDER BY price DESC
                       LIMIT 10
""",conn)

# Query 3 — stock availability count (In Stock vs Out of Stock) → bar chart
q3 = pd.read_sql_query("""
                       SELECT SUM(CASE WHEN availability = 'In stock' THEN 1 ELSE 0 END) as In_Stock,
                              SUM(CASE WHEN availability != 'In stock' THEN 1 ELSE 0 END) as Out_of_stock
                       FROM books
""",conn)

# Query 4 — rating distribution (how many books at each star level 1-5) → bar chart
q4 = pd.read_sql_query("""
                       SELECT star_rating as Rating_in_Stars,
                              COUNT(*) as No_of_Books
                       FROM books
                       GROUP BY star_rating
                       ORDER BY star_rating DESC
                              
""",conn)

# Query 5 — number of books per category → save as CSV only, no chart
q5 = pd.read_sql_query("""
                       SELECT category as Category, count(*) as No_of_Books
                       FROM books
                       GROUP BY category
""",conn)


# Export all 5 as CSVs into reports/. Save 4 charts as PNGs into reports/charts/.
q1.to_csv('reports/category_price_average.csv',index = False)
q2.to_csv('reports/top_10_most_expensive_books.csv',index = False)
q3.to_csv('reports/stock_availability.csv',index = False)
q4.to_csv('reports/rating_distribution.csv',index = False)
q5.to_csv('reports/books_per_category.csv',index = False)
#----------------------------------------------------------------------------------------------------------------------------------------------

# Chart 1
plt.figure(figsize=(8, 10))
bars = plt.barh(q1['category'].iloc[::-1], q1['avg_price'].iloc[::-1])
plt.xlabel('Average Price')
plt.ylabel('Category')
plt.title('Average Price by Category')
plt.tight_layout()
for bar in bars:
        xval = bar.get_width()
        plt.text(xval , bar.get_y() + bar.get_height()/2, f"£{xval:,.2f}", va="center", ha="left")
plt.savefig('reports/charts/avg_price_by_category.png', bbox_inches='tight')
plt.close()

#----------------------------------------------------------------------------------------------------------------------------------------------

# Chart 2
plt.figure(figsize=(10, 6))
bars = plt.barh(q2['title'].iloc[::-1].apply(lambda s: s if len(s) <= 35 else s[:35] + '...')+'...', q2['price'].iloc[::-1])
plt.xlabel('Title')
plt.ylabel('Price')
plt.title('Top 10 Most Expensive Books')
plt.xlim(left=58.5, right=60.5)
plt.tight_layout()
for bar in bars:
        xval = bar.get_width()
        plt.text(xval , bar.get_y() + bar.get_height()/2, f"£{xval:,.2f}", va="center", ha="left")
plt.savefig('reports/charts/top_10_books.png', bbox_inches='tight')
plt.close()

#----------------------------------------------------------------------------------------------------------------------------------------------

# Chart 3

plt.figure(figsize=(6, 4))
bars = plt.bar(q3.iloc[0].index, q3.iloc[0].values, color=['tab:green', 'tab:red'])

plt.title('Stock Availability')
plt.ylabel('Number of Books')
plt.xlabel('Availability')
plt.ylim(0, q3.iloc[0].values.max() * 1.1)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 5,
             f"{int(height)}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig('reports/charts/stock_availability.png', bbox_inches='tight')
plt.close()

#----------------------------------------------------------------------------------------------------------------------------------------------

# Chart 4

plt.figure(figsize=(8, 5))
bars = plt.bar(q4['Rating_in_Stars'].astype(int).astype(str),
               q4['No_of_Books'],
               color='tab:blue')

plt.title('Rating Distribution')
plt.xlabel('Star Rating')
plt.ylabel('Number of Books')
plt.ylim(0, q4['No_of_Books'].max() * 1.1)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2,
             height + 2,
             f"{int(height)}",
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('reports/charts/rating_distribution.png', bbox_inches='tight')
plt.close()