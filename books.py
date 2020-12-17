import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin

import csv

#url d'un livre pour extraction de données
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def scrap_book(url):
    #Récupération d'une page web
    response = requests.get(url)

    #Si l'url est valide, execute le bloc d'instructions suivants
    if response.ok:

        with open("book.csv", mode="w", newline="") as file:
            fieldnames = [  "universal_ product_code (upc)",
                            "price_including_tax", 
                            "price_excluding_tax",
                            "number_available",
                            "product_description",
                            "category",
                            "review_rating",
                            "image_url"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            #Création d'un objet beautifulsoup
            soup = BeautifulSoup(response.text, "lxml")

            #Récupération de la catégorie
            category = soup.select(".breadcrumb > li:nth-child(3) > a")[0].text
            #writer.writerow({"category": category})
            print("La catégorie est :", category)

            #Récupération de la notation avec nombre d'étoiles
            star = soup.find(class_="star-rating")
            notation = star["class"][1]
            #writer.writerow({"review_rating": notation})
            print("La notation du livre est :", notation)

            #Récupération de la description du livre
            description = soup.find("meta", attrs={"name" : "description"}).attrs["content"]
            #writer.writerow({"product_description": description})
            print("La description du livre :", description)

            #Récuperation du lien de l'image de la couverture du livre
            image_url_relative = soup.img.attrs["src"]
            image_url = urljoin("https://books.toscrape.com", image_url_relative)
            #writer.writerow({"image_url": image_url})
            print("L'Url de la couverture du livre est :", image_url)

            #Récupération de différentes données requises du livre
            elements = soup.find_all("td")
            element = ["UPC :"+" "+elements[0].text, "price_including_tax :"+" "+elements[2].text, "price_excluding_tax :"+" "+elements[3].text, "number_available :"+" "+elements[5].text]
            #writer.writerow({"universal_ product_code (upc)": elements[0].text})
            #writer.writerow({"price_including_tax": elements[2].text})
            #writer.writerow({"price_excluding_tax": elements[3].text})
            #writer.writerow({"number_available": elements[5].text})
            print(element)

            #Ecriture dans le fichier csv
            writer.writerow({   "category": category,
                                "review_rating": notation,
                                "product_description": description,
                                "image_url": image_url,
                                "universal_ product_code (upc)": elements[0].text,
                                "price_including_tax": elements[2].text,
                                "price_excluding_tax": elements[3].text,
                                "number_available": elements[5].text
            })

            #Si page web invalide, affiche un message 
    else:
        print("Vérifier l'adresse de la page")



def main():
    scrap_book(url)


if __name__ == "__main__":
    main()