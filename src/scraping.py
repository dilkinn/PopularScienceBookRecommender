import time
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def gr_sign_in(driver):
    login_page = 'https://www.goodreads.com'
    driver.get(login_page)

    username = driver.find_element_by_id("userSignInFormEmail")
    username.clear()
    username.send_keys("*********")
    time.sleep(2)

    password = driver.find_element_by_name("user[password]")
    password.clear()
    password.send_keys("********")
    time.sleep(2)

    driver.find_element_by_xpath("//input[contains(@value,'Sign in')]").click()
    time.sleep(2)
    return driver

## book_links

def scrap_book_links(page1):
    driver = webdriver.Chrome('chromedriver')
    driver = gr_sign_in(driver)
    arr_all = []
    
    driver.get(page1)
    time.sleep(1)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    
    arr = get_book_links_from_soup(soup)
    arr_all.extend(arr)
    
    while True:
        try:
            print("next_page")
            driver.find_element_by_xpath("//a[contains(@rel,'next')]").click()
            time.sleep(1)
            html = driver.page_source
            soup = bs(html, 'html.parser')
            arr = get_book_links_from_soup(soup)
            arr_all.extend(arr)           
        except:
            driver.close()
            break
            
    print(len(arr_all))
    np.array(arr_all)
    df = pd.DataFrame(arr_all)
    df.to_csv(f'../data/book_links_goodreads.csv')
    return df

def get_book_links_from_soup(soup):
    b_links = []
    divs = soup.find_all('a', {"class": "leftAlignedImage"})
    for div in divs:
        b_links.append('http://goodreads.com' + div.get('href'))
    return b_links

def get_the_soup(book_link, driver):
    driver.get(book_link)
    time.sleep(5)
    soup = bs(driver.page_source, 'html.parser')
    print('soup from link ok')
    return soup, driver

def get_isbn(soup):
    isbn_str = soup.find_all('div',{"class":"infoBoxRowItem"})[1].get_text()
    isbn_str = isbn_str.replace('\n', '')
    isbn_str = isbn_str.replace('(', '')
    isbn_str = isbn_str.replace(')', '')
    isbn, isbn13 = isbn_str.strip().split()[0], isbn_str.strip().split()[2]
    print('isbn ok')
    return isbn, isbn13

def get_title(soup):
    title_str = soup.find_all('h1',{"id":"bookTitle"})[0].get_text()
    title_str = title_str.replace('\n', "").strip()
    print('title ok')
    return title_str

def get_avg_rating(soup):
    avg_rating = soup.find_all('span',{"itemprop":"ratingValue"})[0].get_text()
    avg_rating = avg_rating.replace('\n', '').strip()
    avg_rating = float(avg_rating)
    print('avg rating ok')
    return avg_rating

def get_author_name(soup):
    author_name = []
    spans = soup.find_all('a',{"class":"authorName"})[0].find_all('span',{'itemprop':'name'})
    for span in spans:
        author_name.append(span.get_text())
    print('author name ok')
    return author_name

def get_book_desc(soup):
    book_desc = soup.find_all('div',{"id":"description"})[0].find_all('span')[1].get_text()
    print('book description ok')
    return book_desc

def get_genres(soup):
    divs = soup.find_all('a',{"class":"actionLinkLite bookPageGenreLink"})
    genres = []
    for div in divs:
        genres.append(div.get_text())
    print('genres ok')
    return genres

def get_book_info(book_link, soup):
    try:
        isbn, isbn13 = get_isbn(soup)
    except:
        print('********** get_book_info: isbn failed **********')
        param = 'isbn'
        try:
            isbn, isbn13 = try_another_edition(soup, param)
        except:
            print('another edition failed')
            isbn, isbn13 = '0', '0'

    try:
        title_str = get_title(soup) 
    except:
        print('********** get_book_info: title failed **********')
        param = 'book_title'
        try:
            title_str = try_another_edition(soup, param)
        except:
            print('another edition failed')
            title_str = '0'
    
    try:
        avg_rating = get_avg_rating(soup)
    except:
        print('********** get_book_info: rating failed **********')
        param = 'avg_rating'
        try:
            avg_rating = try_another_edition(soup, param)
        except:
            print('another edition failed')
            avg_rating = 0

    author_name = []
    try:
        author_name.extend(get_author_name(soup))
    except:
        print('********** author names failed **********')
        param = 'author_name'
        try:
            author_name.extend(try_another_edition(soup, param))
        except:
            print('another edition failed')
              
    try:
        desc = get_book_desc(soup)
    except:
        print('********** book description failed **********')
        param = 'book_desc'
        try:
            desc = try_another_edition(soup, param)
        except:
            desc = '0'

    try:
        print('trying genres')
        genres = get_genres(soup)
    except:
        print('********** genres failed **********')
        param = 'genres'
        try:
            genres = try_another_edition(soup, param)
        except:
            genres = []
  
    dct = {'book_link': book_link, 'isbn': isbn, 'isbn13': isbn13, 
          'book_title' : title_str, 'avg_rating' : avg_rating, 
          'author_name': author_name, 'book_desc': desc, 'genres': genres}
    
    print('get book info ok')
    return dct


def get_reviews_array_from_soup(soup):
    arr = []
    divs = soup.find_all('div',{"id":"bookReviews"})[0].find_all('div',{'class':'friendReviews elementListBrown'})
    
    for div in divs:
        try:
            user_link = 'http://goodreads.com' + div.find_all('span',{'itemprop':'author'})[0].find('a').get('href')
        except:
            print('No user link')
            user_link = '0'
        try:
            ranking = len(div.find_all('span', {'class':'staticStar p10'}))
        except:
            print('No ranking')
            ranking = '0'
        try:
            review = div.find_all('div', {'class':'reviewText stacked'})[0].find_all('span',{'class':"readable"})[0].find_all('span')[1].get_text()
        except:
            try:
                review = div.find_all('div', {'class':'reviewText stacked'})[0].find_all('span',{'class':"readable"})[0].find_all('span')[0].get_text()
            except:
                review = '0'
                
        dct = {"isbn":isbn, 'user_link': user_link, 'ranking':ranking, "review": review}
        arr.append(dct)
    print(f'get {len(arr)} reviews ok')
    return arr

def get_reviews_from_book_link(isbn, b_l, driver):
    arr_all = []
    
    driver.get(b_l)
    time.sleep(10)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    
    arr = get_reviews_array_from_soup(soup)
    arr_all.extend(arr)
    
    for k in range(1,10):
        try:
            # click next page:
            driver.find_element_by_xpath("//a[contains(@rel,'next')]").click()
            # wait for URL to change with 15 seconds timeout
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "reviews")))
            time.sleep(3)
            html = driver.page_source
            soup = bs(html, 'html.parser')
            arr = get_reviews_array_from_soup(soup)
            arr_all.extend(arr)         
        except:
            try:
                time.sleep(15)
                html = driver.page_source
                soup = bs(html, 'html.parser')
                arr = get_reviews_array_from_soup(soup)
                arr_all.extend(arr)
                print(f'Exception: page {k+1} ok')
            except:
                print(f'Exception: no reviews on page {k+1}!!!!!!!')
    
    print(f'got {len(arr_all)} reviews for this book')
    df = pd.DataFrame(arr_all)
    df.to_csv(f'../data/revs_{isbn}.csv')
    print('reviews file created')
    return df, driver


def try_another_edition(soup, param):
    dct ={}
    divs = soup.find_all('div',{"class":"otherEdition"})
    links = []
    for div in divs:
        link = div.find('a').get('href')
        links.append(link)
        
    for link in links:
        try:
            soup = get_the_soup(link)
            if param == 'isbn':
                isbn, isbn13 = get_isbn(soup)
                if len(isbn) == 10:
                    print('another edition isbn ok')
                    return isbn, isbn13
            elif param == 'book_title':
                title = get_title(soup)
                if len(title) > 0:
                    print('another edition title ok')
                    return title
            elif param == 'avg_rating':
                avg_rating = get_avg_rating(soup)
                print('another edition avg_rating ok')
                return avg_rating
            elif param == 'author_name':
                author_name = get_author_name(soup)
                print('another edition author_name ok')
                return author_name
            elif param == 'book_desc':
                desc = get_book_desc(soup)
                print('another edition book_desc ok')
                return desc
            elif param == 'genres':
                genres = get_genres(soup)
                print('another edition genres ok')
                return genres
        except:
            continue