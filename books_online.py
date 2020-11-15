#import de la librairie requests pour effectuer une requête http
import requests

#import de la librairie beautifulsoup4 pour l'extraction de données en provenance d'un site web
from bs4 import BeautifulSoup

#module pour lecture, écriture au format .csv
import csv

#stockage dans une variable du lien http contenant les données à extraire
url = "http://books.toscrape.com/catalogue/birdsong-a-story-in-pictures_975/index.html"

#Verification de la validité de la requête
response = requests.get(url)
print(response)
