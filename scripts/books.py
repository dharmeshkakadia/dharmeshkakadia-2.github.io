import urllib.request
import urllib.parse
import csv
import json

with open('../_data/books.csv', newline='') as csvfile:
  for row in csv.DictReader(csvfile):
    try:
      urllib.request.urlretrieve(json.load(urllib.request.urlopen('https://www.googleapis.com/books/v1/volumes?q={}'.format(urllib.parse.quote_plus(row['Title']))))['items'][0]['volumeInfo']['imageLinks']['thumbnail'], '../images/books/{}.jpeg'.format(row['Book_Id']))
    except:
      print('Cover not found for {}'.format(row['Title']))
