import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_book_details(book_url):
    """
    Extrai os detalhes de um único livro a partir da sua URL.
    Dados a serem capturados: título, preço, rating, disponibilidade, categoria, imagem[cite: 52].
    """
    try:
        response = requests.get(book_url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extrai os dados
        title = soup.find('h1').text
        price = soup.find('p', class_='price_color').text
        
        # O rating está no nome da classe, ex: "star-rating Five"
        rating_classes = soup.find('p', class_='star-rating')['class']
        rating = f"{rating_classes[1]} de 5 estrelas"

        # A disponibilidade está em um <p> dentro da tabela de informações
        availability = soup.find('p', class_='instock availability').text.strip()
        
        # A categoria está no breadcrumb
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text

        # A URL da imagem precisa ser completada com o domínio base
        image_relative_url = soup.find('div', class_='item active').find('img')['src']
        base_url = 'https://books.toscrape.com/'
        image_url = base_url + image_relative_url.replace('../../', '')

        return {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': availability,
            'category': category,
            'image_url': image_url,
            'book_url': book_url
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {book_url}: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar dados de {book_url}: {e}")
        return None

def scrape_all_books():
    """
    Navega por todas as páginas do site para extrair dados de todos os livros.
    """
    base_url = 'https://books.toscrape.com/catalogue/'
    current_page_url = base_url + 'page-1.html'
    all_books_data = []

    while current_page_url:
        print(f"Coletando dados da página: {current_page_url}")
        
        try:
            response = requests.get(current_page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontra todos os links de livros na página atual
            book_links = [base_url + a['href'] for a in soup.select('h3 > a')]

            for link in book_links:
                book_data = get_book_details(link)
                if book_data:
                    all_books_data.append(book_data)

            # Encontra o link para a próxima página
            next_page_element = soup.find('li', class_='next')
            if next_page_element:
                next_page_url = next_page_element.find('a')['href']
                current_page_url = base_url + next_page_url
            else:
                current_page_url = None # Fim da paginação

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página de listagem {current_page_url}: {e}")
            break # Interrompe o loop em caso de erro de rede

    return all_books_data

def save_to_csv(data, filename='../data/books_data.csv'):
    """
    Salva os dados coletados em um arquivo CSV.
    O caminho é relativo à localização do script.
    """
    if not data:
        print("Nenhum dado para salvar.")
        return

    df = pd.DataFrame(data)
    
    # Garante que o diretório de dados exista
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Dados salvos com sucesso em '{filename}'!")


if __name__ == '__main__':
    print("Iniciando o processo de Web Scraping...")
    scraped_data = scrape_all_books()
    if scraped_data:
        save_to_csv(scraped_data)
    print("Processo de Web Scraping finalizado.")