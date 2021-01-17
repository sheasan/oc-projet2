from urllib.parse import urljoin
import urllib.request
import csv
import book
import parse
import math
import os


url = "https://books.toscrape.com"


def parse_all_books(url):
    """
    La fonction parse_all_books doit être utilisée pour parser et extraire les données de l'ensemble des livres du site
    https://books.toscrape.com uniquement
    """

    # Parsing de la page
    soup = parse.parse_page(url)

    # Création d'une liste vide
    categories_list = []

    # Identification et extraction des différents lien de catégories contenu dans la balise a
    categories = soup.find(class_="nav nav-list").find_all("a")

    # Variable contenant l'adresse du home directory de l'utilisateur
    home = os.path.expanduser("~")

    # Création d'un répertoire pour les fichiers csv et image
    try:
        os.mkdir(home+"/data")
    except FileExistsError:
        pass

    try:
        os.mkdir(home+"/data/csv_files")
    except FileExistsError:
        pass

    try:
        os.mkdir(home+"/data/pictures")
    except FileExistsError:
        pass

    # Parcourir la liste des catégories pour transformer l'url relatif en url complet des catégories par une jointure
    for category in categories[1:]:
        relative_link = category.get("href")
        absolute_link = urljoin("https://books.toscrape.com", relative_link)
        categories_list.append(absolute_link)

    # Pour chaque catégorie déterminer la pagination
    for category_url in categories_list:
        parse_category_page = parse.parse_page(category_url)

        # Extraction du nom de la catégorie
        category_name = parse_category_page.h1.text

        # Création d'une liste vide pour stocker les données de dictionnaires
        dict_data_list_by_category = []

        # Obtenir le nombre de pages par catégorie
        parse_books_quantity = parse_category_page.select(".form-horizontal > strong:nth-child(2)")[0].text

        # Gestion des erreurs lors de la conversion
        try:
            books_quantity_number = int(parse_books_quantity)
        except ValueError:
            # Mettre un petit texte explicatif pour l'utilisateur si conversion impossible
            books_quantity_number = 0
            print("La conversion est impossible, une valeur par défaut a été appliquée : 0")

        books_quantity_per_page = 20

        # Déterminer la pagination par catégorie
        pages_number = math.ceil(books_quantity_number/books_quantity_per_page)

        #  Parcourir les différentes pages des catégories (utilisation opérateur ternaire)
        for i in range(1, pages_number+1):
            page_url = urljoin(category_url, f"page-{i}.html") if i > 1 else category_url

            # Parsing de chaque page de la catégorie en vue d'extraire les données
            each_parsed_category_page = parse.parse_page(page_url)

            # Identifier la balise contenant le titre, lien de chaque livre par page parsée
            books_subtitles = each_parsed_category_page.find_all("h3")

            # Obtenir le lien complet de chaque livre et effectuer un parsing (meux cibler, les a dans h3) ==> Fair une comprehension de liste qui va directmement appliquer la ligne 84 et 85 (avant le for)
            for iteration, book_subtitle in enumerate(books_subtitles):

                # Extraction des liens relatifs de chaque livre de la page
                partial_books_links = book_subtitle.a.get("href").replace("../../..", "catalogue")

                # Reconstitution du lien absolu des livres de la page avec une jointure
                complete_books_links = urljoin("https://books.toscrape.com", partial_books_links)

                # Extraction des différentes données de chaque livre en utilisation une fonction
                book_data = book.scrap_book(complete_books_links)

                # Gestion des caractères spéciaux avec ajout devant le titre d'un chiffre unique pour chaque iteration
                clean_title = str(iteration)+"."+book_data["title"].replace("/", "_")

                # Ajout des données de chaque livre scrapé dans la liste
                dict_data_list_by_category.append(book_data)

                # Telechargement de l'image de la couverture du livre
                urllib.request.urlretrieve(book_data["image_url"], home+"/data/pictures/"+clean_title)

                # Réassignation de l'emplacement local pour l'image url du dictionnaire
                book_data["image_url"] = home+"/data/pictures/"+clean_title

        # Ecriture dans fichier CSV de tous les éléments de la liste
        csv_columns = ["product_page_url",
                       "universal_ product_code (upc)",
                       "title", "price_including_tax",
                       "price_excluding_tax",
                       "number_available",
                       "product_description",
                       "category", "review_rating",
                       "image_url"]
        csv_file = category_name+".csv"
        try:
            with open(home+"/data/csv_files/"+csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data_list_by_category:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


parse_all_books(url)
