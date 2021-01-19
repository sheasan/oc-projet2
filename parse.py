import requests
from bs4 import BeautifulSoup


def parse_page(url):
    """La fonction parse_page() effectue le parsing d'un site internet à partir de son lien url"""
    response = requests.get(url)
    if response.ok:
        parse_page = BeautifulSoup(response.content, "lxml")
        print("cocorico")
    else:
        print("Vérifier l'url")
    return parse_page


def main():
    parse_page()


if __name__ == "__main__":
    main()
