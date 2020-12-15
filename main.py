import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin

import csv

url = "https://books.toscrape.com/catalogue/page-1.html"

#Récupération d'une page web
response = requests.get(url)

#Si l'url est valide, execute le bloc d'instructions suivants
if response.ok:

    #Création d'un objet beautifulsoup
    soup = BeautifulSoup(response.text, "lxml")

    subtitles = soup.find_all("h3")

    for subtitle in subtitles:
        partial_books_links = subtitle.a.get("href")
        complete_books_links = urljoin("https://books.toscrape.com/catalogue/", partial_books_links)
        #print(complete_books_links)

for i in range(1, 51):
    page_number = i
    page_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    print(page_url)
