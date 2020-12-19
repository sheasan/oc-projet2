import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import csv
import books
import math


'''with open("scrapfile.csv", mode="w", newline="") as file:
    fieldnames = ["product_page_url",
                  "universal_ product_code (upc)",
                  "title",
                  "price_including_tax", 
                  "price_excluding_tax",
                  "number_available",
                  "product_description",
                  "category",
                  "review_rating",
                  "image_url"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, 3):
        page_number = i
        page_url = f"https://books.toscrape.com/catalogue/page-{i}.html"

        response = requests.get(page_url)
        if response.ok:
            soup = BeautifulSoup(response.text, "lxml")
            subtitles = soup.find_all("h3")

        

            for subtitle in subtitles:
                partial_books_links = subtitle.a.get("href")
                complete_books_links = urljoin("https://books.toscrape.com/catalogue/", partial_books_links)
                #writer.writerow([complete_books_links])
                print("L'url du livre est :", complete_books_links)
                all_data_books = books.scrap_book(complete_books_links)

                #Telechargement et enregistrement de l'image
                urllib.request.urlretrieve(books.scrap_book.book_data["image_url"], books.scrap_book.book_data["title"])

                writer.writerow({"product_page_url": complete_books_links,
                                 "universal_ product_code (upc)": books.scrap_book.book_data["universal_ product_code (upc)"],
                                 "title": books.scrap_book.book_data["title"],
                                 "price_including_tax": books.scrap_book.book_data["price_including_tax"],
                                 "price_excluding_tax": books.scrap_book.book_data["price_excluding_tax"],
                                 "number_available": books.scrap_book.book_data["number_available"],
                                 "product_description": books.scrap_book.book_data["product_description"],
                                 "category": books.scrap_book.book_data["category"],
                                 "review_rating": books.scrap_book.book_data["review_rating"],
                                 "image_url": books.scrap_book.book_data["image_url"]})
    else:
        print("Vérifier l'url")'''

url = "https://books.toscrape.com"

def parse_page(url):
    response = requests.get(url)
    if response.ok:
        parse_page.soup = BeautifulSoup(response.text, "lxml")
    return parse_page.soup


response = requests.get(url)

category_list = []
if response.ok:
    soup = BeautifulSoup(response.text, "lxml")
    # Identification et extraction des catégories
    categorys = soup.find(class_="nav nav-list").find_all("a")
    for category in categorys[1:]:
        relative_link = category.get("href")
        absolute_link = urljoin("https://books.toscrape.com", relative_link)
        category_list.append(absolute_link)

    # Pour chaque catégorie déterminer la pagination
    for category_element in category_list:
        parse_page(category_element)

        # Obtenir le nombre de pages par catégorie
        parse_books_quantity = parse_page.soup.select(".form-horizontal > strong:nth-child(2)")[0].text
        books_quantity_result = int(parse_books_quantity)
        books_quantity_per_page = 20
        pages_number = math.ceil(books_quantity_result/books_quantity_per_page)

        # Si il y'a plus d'une page dans la catégorie
        if pages_number > 1:

            for i in range(1, pages_number+1):
                page_url = urljoin(category_element, f"page-{i}.html")
                parse_page(page_url)

                soup = BeautifulSoup(response.text, "lxml")
                subtitles = soup.find_all("h3")

                for subtitle in subtitles:
                    partial_books_links = subtitle.a.get("href")
                    print(partial_books_links)
                    complete_books_links = urljoin("https://books.toscrape.com", partial_books_links)
                    print("L'url du livre est :", complete_books_links)
                    all_data_books = books.scrap_book(complete_books_links)


        else:
            print("wait")



