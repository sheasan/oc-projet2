import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import argparse

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


def scrap_book(url):

    # Récupération d'une page web
    response = requests.get(url)

    # Si l'url est valide, execute le bloc d'instructions suivants
    if response.ok:

        # Création d'un objet beautifulsoup
        soup = BeautifulSoup(response.text, "lxml")

        # Récupération du titre du livre
        title = soup.h1.string
        # book_data["title"] = title
        print("Le titre du livre est :", title)

        # Récupération de la catégorie
        category = soup.select(".breadcrumb > li:nth-child(3) > a")[0].text
        # book_data["category"] = category
        print("La catégorie est :", category)

        # Récupération de la notation avec nombre d'étoiles
        star = soup.find(class_="star-rating")
        notation = star["class"][1]
        # book_data["review_rating"] = notation
        print("La notation du livre est :", notation)

        # Récupération de la description du livre
        description = soup.find("meta", attrs={"name" : "description"}).attrs["content"]
        # book_data["product_description"] = description
        print("La description du livre :", description)

        # Récuperation du lien de l'image de la couverture du livre
        image_url_relative = soup.img.attrs["src"]
        image_url = urljoin("https://books.toscrape.com", image_url_relative)
        # book_data["image_url"] = image_url
        print("L'Url de la couverture du livre est :", image_url)

        # Récupération de différentes données requises du livre
        elements = soup.find_all("td")
        element = ["UPC :"+" "+elements[0].text, "price_including_tax :"+" "+elements[2].text, "price_excluding_tax :"+" "+elements[3].text, "number_available :"+" "+elements[5].text]
        print(element)

        scrap_book.book_data = {
            "product_page_url" : None,
            "universal_ product_code (upc)": elements[0].text,
            "title": title,
            "price_including_tax": elements[2].text,
            "price_excluding_tax": elements[3].text,
            "number_available": elements[5].text,
            "product_description": description,
            "category": category,
            "review_rating": notation,
            "image_url": image_url
        }
        #print(book_data)
    else:
        print("Vérifier l'url")
    return scrap_book.book_data


def main(args):
    scrap_book(args.url)

#Utilisation du module Argparse pour entrer le paramètre de la fonction en ligne de commande
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="url par live du site https://books.toscrape.com pour scraping")
    parser.add_argument("--url", type=str, help="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000")
    args = parser.parse_args()
    main(args)
