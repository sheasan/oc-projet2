import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import csv
import book
import math
import os


url = "https://books.toscrape.com"


def parse_page(url):
    """La fonction parse_page() effectue le parsing d'un site internet à partir de son lien url"""
    response = requests.get(url)
    if response.ok:
        parse_page = BeautifulSoup(response.content, "lxml")
    else:
        print("Vérifier l'url")
    return parse_page


def parse_all_books(url):

    """
    La fonction parse_all_books doit être utilisée pour parser et extraire les données de l'ensemble des livres du site
    https://books.toscrape.com uniquement
    """

    # Parsing de la page
    soup = parse_page(url)

    # Création d'une liste vide
    categories_list = []

    # Identification et extraction des catégories
    categories = soup.find(class_="nav nav-list").find_all("a")

    # Création d'un répertoire pour les fichiers csv et image
    os.mkdir("/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data")
    os.mkdir("/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data/csv_files")
    os.mkdir("/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data/pictures")

    # Parcourir la liste des catégories pour obtenir l'url complet de chaque catégorie
    for category in categories[1:]:
        relative_link = category.get("href")
        absolute_link = urljoin("https://books.toscrape.com", relative_link)
        categories_list.append(absolute_link)

    # Pour chaque catégorie déterminer la pagination
    for category_url in categories_list:
        parse_category_page = parse_page(category_url)
        category_name = parse_category_page.h1.text

        # Création d'une liste vide pour stocker les données de dictionnaires
        dict_data_list_by_category = []

        # Obtenir le nombre de pages par catégorie
        parse_books_quantity = parse_category_page.select(".form-horizontal > strong:nth-child(2)")[0].text
        books_quantity_number = int(parse_books_quantity)
        books_quantity_per_page = 20
        pages_number = math.ceil(books_quantity_number/books_quantity_per_page)

        # Déterminer la pagination par page de catégorie
        for i in range(1, pages_number+1):
            if i > 1:
                page_url = urljoin(category_url, f"page-{i}.html")
            else:
                page_url = category_url

            each_parsed_category_page = parse_page(page_url)
            books_subtitles = each_parsed_category_page.find_all("h3")

            for iteration, book_subtitle in enumerate(books_subtitles):
                partial_books_links = book_subtitle.a.get("href").replace("../../..", "catalogue")
                complete_books_links = urljoin("https://books.toscrape.com", partial_books_links)
                book_data = book.scrap_book(complete_books_links)

                # Gestion des caractères spéciaux
                clean_title = str(iteration)+"."+book_data["title"].replace("/", "_")

                # Ajout du lien url de la page du livre dans le dictionnaire
                book_data["product_page_url"] = complete_books_links

                # Ajout des données de chaque livre scrapé dans la liste
                dict_data_list_by_category.append(book_data)

                # Telechargement de l'image de la couverture du livre
                urllib.request.urlretrieve(book_data["image_url"], "/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data/pictures/"+clean_title)

                # Réassignation de l'emplacement local pour l'image url du dictionnaire
                book_data["image_url"] = "/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data/pictures/"+clean_title
    
        # Ecriture dans fichier CSV de tous les éléments de la liste
        csv_columns = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
        csv_file = category_name+".csv"
        try:
            with open("/home/ali/Documents/Openclassrooms/Projets/oc-projet2/data/csv_files/"+csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data_list_by_category:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
    

parse_all_books(url)
