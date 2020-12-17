import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin

import csv

import books

#url = "https://books.toscrape.com/catalogue/page-1.html"

#Récupération d'une page web
#response = requests.get(url)

#Si l'url est valide, execute le bloc d'instructions suivants
#if response.ok:

'''#Création d'un objet beautifulsoup
    soup = BeautifulSoup(response.text, "lxml")

    #Récupération de l'ensemble des titre de balise h3 sur la page
    subtitles = soup.find_all("h3")

    #Parcourir les titres h3 et récupération du lien des livres de la page contenu dans la balise a
    for subtitle in subtitles:
        partial_books_links = subtitle.a.get("href")
        complete_books_links = urljoin("https://books.toscrape.com/catalogue/", partial_books_links)
        #print(complete_books_links)'''

for i in range(1, 2):
    page_number = i
    page_url = f"https://books.toscrape.com/catalogue/page-{i}.html"


    response = requests.get(page_url)
    if response.ok:

        soup = BeautifulSoup(response.text, "lxml")

        subtitles = soup.find_all("h3")

        with open("scrapfile.csv", mode="w", newline="") as file:
            fieldnames = [  "product_page_url",
                            "universal_ product_code (upc)",
                            "price_including_tax", 
                            "price_excluding_tax",
                            "number_available",
                            "product_description",
                            "category",
                            "review_rating",
                            "image_url"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for subtitle in subtitles:
                partial_books_links = subtitle.a.get("href")
                complete_books_links = urljoin("https://books.toscrape.com/catalogue/", partial_books_links)
                #writer.writerow([complete_books_links])
                print("L'url du livre est :", complete_books_links)
                all_data_books = books.scrap_book(complete_books_links)

                writer.writerow({"product_page_url": complete_books_links,
                                 "category": books.category,
                                 "review_rating": books.notation,
                                 "product_description": books.description,
                                 "image_url": books.image_url,
                                 "universal_ product_code (upc)": books.elements[0].text,
                                 "price_including_tax": books.elements[2].text,
                                 "price_excluding_tax": books.elements[3].text,
                                 "number_available": books.elements[5].text
            })


                




    
