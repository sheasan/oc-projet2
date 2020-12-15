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

        #Création d'un objet beautifulsoup
        soup = BeautifulSoup(response.text, "lxml")

        #Récupération de la catégorie
        category = soup.select(".breadcrumb > li:nth-child(3) > a")[0].text
        print("La catégorie est :", category)

        #Récupération de la notation avec nombre d'étoiles
        star = soup.find(class_="star-rating")
        print("La notation du livre est :", star["class"][1])

        #Récupération de la description du livre
        description = soup.find("meta", attrs={"name" : "description"}).attrs["content"]
        print("La description du livre :", description)

        #Récuperation du lien de l'image de la couverture du livre
        image_url_relative = soup.img.attrs["src"]
        image_url = urljoin("https://books.toscrape.com", image_url_relative)
        print("L'Url de la couverture du livre est :", image_url)

        #Récupération de différentes données requises du livre
        elements = soup.find_all("td")
        element = ["UPC :"+" "+elements[0].text, "price_including_tax :"+" "+elements[2].text, "price_excluding_tax :"+" "+elements[3].text, "number_available :"+" "+elements[5].text]
        print(element)

    #Si page web invalide, affiche un message 
    else:
        print("Vérifier l'adresse de la page")




def main():
    scrap_book()


if __name__ == "__main__":
    main()