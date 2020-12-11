#import de la librairie requests pour effectuer une requête http
import requests

#import de la librairie beautifulsoup4 pour l'extraction de données en provenance d'un site web
from bs4 import BeautifulSoup

#import librairie urllib pour jointure d'url
from urllib.parse import urljoin

#module pour lecture, écriture au format .csv
import csv


def scrap_book_page(url):
    response = requests.get(url)
    if response.ok:

        #Créer un dictionnaire pour enregistrer chacunes des valeurs dedans
        soup = BeautifulSoup(response.text, "lxml")
        title = soup.h1.string
        print("Le titre du livre est :", title)

        star = soup.find(class_="star-rating")
        print("La notation du livre est :", star["class"])

        description = soup.find("meta", attrs={"name" : "description"}).attrs["content"]
        print("La description du livre :", description)

        image_url_relative = soup.img.attrs["src"]
        image_url = urljoin("https://books.toscrape.com", image_url_relative)
        print("L'Url de la couverture du livre est :", image_url)

        elements = soup.find_all("td")
        print(elements)

        #Retourner le dictionnaire préalablement associé avec valeurs

    else:
        print("KO")


def main():
    scrap_book_page()

if __name__ == "__main__":
    main()