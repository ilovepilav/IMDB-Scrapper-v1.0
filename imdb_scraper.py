import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Create a list for target URLs
reqUrls =list() 

def MainMethod(): # Basically just capture IMDB Top 250 movies' links and append it to our list.
    url = 'https://www.imdb.com/chart/top/'
    req = requests.get(url)
    page = req.content
    main_url_string = 'https://www.imdb.com'

    soup = BeautifulSoup(page,'html.parser')

    link_soups = soup.find_all('td', class_='titleColumn')

    for link in link_soups:
        url = link.find('a')
        reqUrls.append(f"{main_url_string+url.get('href')}")
    req.close()


def ScrapeData():
    f = open('imdb_top250.txt','a') # Create a text file
    f.write(f'title,rating,year,genre,director,stars,summary') # Column names for future csv integrating
    f.write('\n')

    for x in reqUrls: # Making readable and usable data texts which gathered from beatifulsoup html parser with string methods.
        xsoup = BeautifulSoup(requests.get(x).content,'html.parser')
        title = (xsoup.find('h1').text).strip('\n')
        title = title[:title.index(' (')]
        rating = (xsoup.find('div',class_='ratingValue').text).strip('\n')
        rating = rating[:rating.index('/10')]
        year = xsoup.find('span',id='titleYear').text
        year = year.strip('(').strip(')')
        genre_soup = xsoup.findAll('div', class_='see-more inline canwrap')
        genre=''
        for gs in genre_soup:
            genre += f'{gs.a.text},'
        genre = genre.rstrip(',').lstrip(' ')
        director = xsoup.find('div', class_='credit_summary_item').a.text
        stars_soup = xsoup.find_all('div', class_='credit_summary_item')
        stars = ''
        for st in stars_soup:
            stars+=f'{st.a.text},'
        stars = stars.rstrip(',').lstrip(f'{director},')
        summary = (xsoup.find('div',class_='inline canwrap').text)
        if 'Written by' in summary:
            summary = summary[:summary.index('Written by')].strip('\n').lstrip(' ')
            summary = summary.replace('"','')
        else:
            summary = summary.strip('\n').lstrip(' ')
            summary = summary.replace('"','')
        element = f'"{title}",{rating},{year},"{genre}",{director},"{stars}","{summary}"' # Ordered the strings
        f.write(element) # Write it to text file.
        f.write('\n')
    f.close()

def CsvConverter(): # Convert txt file to CSV 
    read_file = pd.read_csv('imdb_top250.txt', delimiter=',', quotechar='"', engine='python')
    read_file.to_csv('imdb_top250.csv')

MainMethod() # Top 250 link gatherer
ScrapeData() # Data scraper and modifier
CsvConverter() # Txt>CSV converter.
