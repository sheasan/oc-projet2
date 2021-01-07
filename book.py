import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse


def scrap_book(url):
    """
    Extrait les différentes données d'un livre à partir d'un lien url d'un livre du site https://books.toscrape.com/
    """

    # Récupération d'une page web
    response = requests.get(url)

    # Si l'url est valide, execute le bloc d'instructions suivants
    if response.ok:

        # Création d'un objet beautifulsoup
        soup = BeautifulSoup(response.content, "lxml")

        # Récupération du titre du livre
        title = soup.h1.string

        # Récupération de la catégorie
        category = soup.select(".breadcrumb > li:nth-child(3) > a")[0].text

        # Récupération de la notation avec nombre d'étoiles
        star = soup.find(class_="star-rating")
        notation = star["class"][1]

        # Récupération de la description du livre
        description = soup.find("meta", attrs={"name" : "description"}).attrs["content"]

        # Récuperation du lien de l'image de la couverture du livre
        image_url_relative = soup.img.attrs["src"]
        image_url = urljoin("https://books.toscrape.com", image_url_relative)

        # Récupération de différentes données requises du livre
        elements = soup.find_all("td")

        # Extraction du number available et nettoyage pour obtenir que le nombre
        number_available_string = elements[5].text
        number_available_string_list = number_available_string.split()
        number_string = number_available_string_list[2].replace("(", "")
        number = int(number_string)

        book_data = {
            "product_page_url" : url,
            "universal_ product_code (upc)": elements[0].text,
            "title": title,
            "price_including_tax": elements[2].text,
            "price_excluding_tax": elements[3].text,
            "number_available": number,
            "product_description": description,
            "category": category,
            "review_rating": notation,
            "image_url": image_url
        }
    else:
        print("Vérifier l'url")
    return book_data


def main(args):
    print(scrap_book(args.url))


# Utilisation du module Argparse pour entrer le paramètre de la fonction en ligne de commande
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="url par live du site https://books.toscrape.com pour scraping")
    parser.add_argument("--url", type=str, help="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000")
    args = parser.parse_args()
    main(args)
