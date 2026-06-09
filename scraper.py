import requests
from bs4 import BeautifulSoup
import pandas as pd 
import matplotlib.pyplot as plt
import time
import os

URL = 'https://books.toscrape.com/'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

navigation = soup.find('ul', class_ = 'nav nav-list')

cat_dict = {}
titles = []
prices = []
star_rating = []
availability_list = []
categories = []

for li in navigation.find_all('li')[1:]:
    category = li.find('a').text.strip()
    cat_link = URL+li.find('a')['href'].strip()
    cat_dict[f'{category}'] = f'{cat_link}'

# def printnexturl(url):
#     print(url)
#     new_page = requests.get(url)
#     soup = BeautifulSoup(new_page.content, 'html.parser')
#     pager = soup.find('ul', class_ = 'pager')
#     if pager:
#         next_link_tag = pager.find('li', class_ = 'next')
#         if next_link_tag:
#             if next_link_tag.find('a'):
#                 next_link_tag = next_link_tag.find('a')
#                 printnexturl(url[:url.rfind('/')+1]+next_link_tag['href'])

# for i in cat_dict.keys():
#     category = i
#     url = cat_dict[i]
#     print(url)
#     new_page = requests.get(url)
#     soup = BeautifulSoup(new_page.content, 'html.parser')
#     pager = soup.find('ul', class_ = 'pager')
#     if pager:
#         next_link_tag = pager.find('li', class_ = 'next')
#         if next_link_tag:
#             if next_link_tag.find('a'):
#                 next_link_tag = next_link_tag.find('a')
#                 printnexturl(url[:url.rfind('/')+1]+next_link_tag['href'])

def getpagedata(category, url, titles, prices, star_rating, categories, availability_list):
    new_page = requests.get(url)
    soup = BeautifulSoup(new_page.content, 'html.parser')
    books = soup.find('ol', class_ = 'row').find_all('li')
    title = ''
    price = 0
    rating = 0
    availability = ''

    for book in books:
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_ = 'price_color').text
        rating = book.find('p').get('class')
        availability = book.find('p', class_ = 'instock availability').text.strip()
        titles.append(title)
        prices.append(price)
        star_rating.append(rating)
        availability_list.append(availability)
        categories.append(category)
    
    pager = soup.find('ul', class_ = 'pager')
    if pager:
        next_link_tag = pager.find('li', class_ = 'next')
        if next_link_tag:
            if next_link_tag.find('a'):
                next_url = url[:url.rfind('/')+1] + next_link_tag.find('a')['href']
                titles, prices, star_rating, categories, availability_list = getpagedata(category, next_url, titles, prices, star_rating, categories, availability_list)

    return titles, prices, star_rating, categories, availability_list
    


def getdata(cat_dict, titles, prices, star_rating, categories, availability_list):
    for i in cat_dict.keys():
        category = i
        url = cat_dict[i]
        titles, prices, star_rating, categories, availability_list = getpagedata(category, url, titles, prices, star_rating, categories, availability_list)
    return titles, prices, star_rating, categories, availability_list

        

titles, prices, star_rating, categories, availability_list = getdata(cat_dict, titles, prices, star_rating, categories, availability_list)

df = pd.DataFrame({
    'title': titles,
    'price': prices,
    'star_rating': star_rating,
    'category': categories,
    'availability': availability_list
})

df.to_csv('data/raw/books_raw.csv', index = False)