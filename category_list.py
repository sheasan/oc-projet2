#import de la librairie requests pour effectuer une requête http
import requests

#import de la librairie beautifulsoup4 pour l'extraction de données en provenance d'un site web
from bs4 import BeautifulSoup

#import librairie urllib pour jointure d'url
from urllib.parse import urljoin

#module pour lecture, écriture au format .csv
import csv

#import librairie argparse
import argparse


#import 
import books_by_category
import books_online

'''url = "https://books.toscrape.com"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, "lxml")
    categorys = soup.find(class_="nav nav-list").select("a")
    url_category = []
    for category in categorys[1:]:
        url_category = urljoin("https://books.toscrape.com/catalogue", category.get("href"))
        print(url_category)'''

def scrap_category(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        categorys = soup.find(class_="nav nav-list").select("a")
        url_category = []
        for category in categorys[1:]:
            url_category = urljoin("https://books.toscrape.com/catalogue", category.get("href"))
            print(url_category)

            #Appel de la fonction pour scraper chaque livre(lien) par catégorie
            books_list_by_category = books_by_category.scrap_books_category(url_category)
            

            #Appel de la fonction pour scrapper les éléments d'un livre
            each_books_elements = books_online.scrap_book_page(books_list_by_category)
            #print(books_list_by_category)


scrap_category("https://books.toscrape.com")