#import de la librairie requests pour effectuer une requête http
import requests

#import de la librairie beautifulsoup4 pour l'extraction de données en provenance d'un site web
from bs4 import BeautifulSoup

#import librairie urllib pour jointure d'url
from urllib.parse import urljoin

#module pour lecture, écriture au format .csv
import csv

url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/page-3.html"


def scrap_books_category(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.ol.find_all("div", class_="image_container")
        for link in links:
            for link_book in link.find_all("a"):
                link_absolute = urljoin(url, link_book.get("href"))
                print(link_absolute)

    while True:
        try:
            page_number = soup.find("li", class_="next").a
            page_number_link = urljoin(url, page_number.get("href"))
            print(page_number_link)      
            break
        except AttributeError:
            pass
            break
def main():
    scrap_books_category(url)

if __name__ == "__main__":
    main()