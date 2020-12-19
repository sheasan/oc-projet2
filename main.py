import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import csv
import books


with open("scrapfile.csv", mode="w", newline="") as file:
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
        print("Vérifier l'url")