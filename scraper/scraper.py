"""
BookScraper - Web Scraper para books.toscrape.com

Este script realiza web scraping no site books.toscrape.com, navegando por todas as páginas de livros,
extraindo informações detalhadas de cada livro e salvando os resultados em um arquivo CSV.

Funcionalidades:
- Percorre todas as páginas de listagem de livros.
- Para cada livro, extrai: título, preço, estoque, descrição, avaliação em estrelas, URL da imagem e categoria.
- Salva os dados extraídos em 'books.csv'.
- Utiliza variáveis de ambiente (SCRAPE_URL) carregadas de um arquivo .env.
- Registra logs do processo de scraping.

Dependências:
- requests
- beautifulsoup4
- python-dotenv

Como usar:
1. Defina a variável SCRAPE_URL no arquivo .env (exemplo: SCRAPE_URL=https://books.toscrape.com/).
2. Execute o script: python scraper.py
3. O resultado estará no arquivo books.csv.

Autor: Luiz Pedro Scariot
"""

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import csv
from urllib.parse import urljoin
import logging

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class BookScraper:
    """
    Classe responsável por realizar o scraping dos livros.
    """
    def __init__(self):
        """
        Inicializa o scraper com a URL base definida na variável de ambiente SCRAPE_URL.
        """
        self.base_url = os.environ.get("SCRAPE_URL")

    def __scrape(self, url: str) -> BeautifulSoup:
        """
        Realiza o download e parsing HTML de uma página.

        Args:
            url (str): URL da página a ser baixada.

        Returns:
            BeautifulSoup: Objeto soup da página.
        """
        logging.info(f"Scraping URL: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def __books_list(self):
        """
        Percorre todas as páginas de livros e extrai os dados de cada livro.

        Returns:
            list: Lista de dicionários com os dados dos livros.
        """
        books = []
        next_page_url = self.base_url
        page_count = 1
        while next_page_url:
            logging.info(f"Processando página {page_count}: {next_page_url}")
            soup = self.__scrape(next_page_url)
            for book in soup.select('article.product_pod'):
                url_aux = book.h3.a['href']
                book_url = urljoin(next_page_url, url_aux)
                logging.info(f"Extraindo livro: {book_url}")
                book_soup = self.__scrape(book_url)
                title = book_soup.select_one('div.product_main h1').text
                price = book_soup.select_one('p.price_color').text
                stock = book_soup.select_one('p.instock.availability').text.strip()
                description_tag = book_soup.select_one('div#product_description + p')
                description = description_tag.text if description_tag else ''
                stars = book_soup.select_one('p.star-rating')['class'][1]
                img_tag = book_soup.select_one('div#product_gallery img')
                img_url = urljoin(book_url, img_tag['src']) if img_tag else ''
                breadcrumb = book_soup.select('ul.breadcrumb li a')
                category = breadcrumb[-1].text if len(breadcrumb) > 2 else ''
                books.append({
                    'title': title,
                    'price': price,
                    'stock': stock,
                    'description': description,
                    'stars': stars,
                    'img_url': img_url,
                    'category': category
                })
            next_li = soup.select_one('li.next a')
            if next_li:
                next_href = next_li['href']
                next_page_url = urljoin(next_page_url, next_href)
                page_count += 1
            else:
                next_page_url = None
        logging.info(f"Total de livros extraídos: {len(books)}")
        return books

    @staticmethod
    def execute():
        """
        Executa o scraping e retorna a lista de livros extraídos.

        Returns:
            list: Lista de dicionários com os dados dos livros.
        """
        scraper = BookScraper()
        return scraper.__books_list()

if __name__ == "__main__":
    results = BookScraper.execute()
    logging.info("Salvando resultados em books.csv")
    with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
        if results:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        else:
            csvfile.write('No data found\n')
    logging.info("Execução finalizada.")