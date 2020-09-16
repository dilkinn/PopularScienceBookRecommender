import goodreads_api_client as gr
from bs4 import BeautifulSoup as bs
import requests
import numpy as np

from urllib.request import urlopen
import re

def get_the_link_from_widget(widget):
    soup = bs(widget, 'html')
    link = soup.find('iframe', {"id":"the_iframe"}).get('src')

    return link

def get_the_link(isbn_number):
    client = gr.Client(developer_key='fGkJVZsWA7At7eDPqUec4A')
    book = client.Book.show_by_isbn(isbn=isbn_number)
    keys_wanted = ['id', 'title', 'isbn', 'reviews_widget']
    reduced_book = {k:v for k, v in book.items() if k in keys_wanted}
    widget = reduced_book['reviews_widget']
    link = get_the_link_from_widget(widget)
    return link

def get_div_reviews(link):
    '''Returns div containers list from the page with link.'''
    r = requests.get(link)
#     print(r.status_code)
    soup = bs(r.content, "html")
    # print(soup.prettify())
    div_reviews = soup.find_all("div", {"class": "gr_review_container"})
    return div_reviews

def get_all_pages(page_1):
    '''Returns a list of all pages srarting with page_1.'''
    links = []
    link = page_1
    i = 0
    while True:
        links.append(link)
        try:
            r = requests.get(link)
#             print(r.status_code)
            soup = bs(r.content, "html")
            next_link = 'http://goodreads.com/' + soup.find_all("a", {"class":"next_page"})[0].get("href")
            link = next_link
        except IndexError:
            print("No more reviews")
            break
    return links

def div_reviews_all_pages(pages):
    div_reviews = []
    for page in pages:
        div_reviews.extend(get_div_reviews(page))
    return div_reviews

def get_the_rating(div):
    try:
        stars = div.find_all('span',{"class":"gr_rating"})[0].contents[0]
        rating = 0
        for star in stars:
            black = '★'
            if star == black:
                rating += 1
    except:
        rating = np.nan
    return rating

def get_review(div):
    '''Returns div containers list from the page with link.'''
    full_review_link = div.find_all('a',{"class":"gr_more_link"})[0].get('href')
    
    r = requests.get(full_review_link)
#     print(r.status_code)
    soup = bs(r.content, "html")
    # print(soup.prettify())
    lst = soup.find_all("div", {"class": "reviewText mediumText description readable"})[0].contents
    lst_new = []
    for el in lst:
        el = str(el)
        if el[0] != '<' and el[-1] != '>':
            lst_new.append(el)
    review = " ".join(lst_new)
    reviewer_full_name = soup.find_all("a", {"class": "userReview"})[0].contents[0]
    reviewer_link = soup.find_all("a", {"class": "userReview"})[0].get('href')
    return review, reviewer_full_name, reviewer_link