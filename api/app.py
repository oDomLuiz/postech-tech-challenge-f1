from flask import Flask, jsonify, request
import pandas as pd
import os
from flasgger import Swagger
import numpy as np

# Inicializa a aplicação Flask
app = Flask(__name__)

# Carrega as configurações do arquivo config.py
app.config.from_object('config')

# Configura o Flasgger (Swagger)
swagger = Swagger(app)

# Define o caminho para o arquivo CSV
DATA_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'books_data.csv'))

def load_books_data():
    """
    Carrega os dados do arquivo CSV, adiciona um 'id' e limpa/converte 
    as colunas 'price' e 'rating' para valores numéricos.
    """
    try:
        if not os.path.exists(DATA_FILE_PATH):
            return None
            
        df = pd.read_csv(DATA_FILE_PATH)
        
        # 1. Adiciona ID
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'id'}, inplace=True)
        
        # 2. Limpa e converte 'price'
        # Remove o símbolo '£' e converte para float
        if 'price' in df.columns:
            df['price_numeric'] = df['price'].replace({r'[£]': ''}, regex=True).astype(float)
        
        # 3. Limpa e converte 'rating'
        # Mapeia o texto da avaliação (ex: "Five") para um número (ex: 5)
        if 'rating' in df.columns:
            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }
            # Extrai a primeira palavra (ex: "Five") e a mapeia
            df['rating_numeric'] = df['rating'].str.split(' ').str[0].map(rating_map)
            
        return df
        
    except Exception as e:
        print(f"Erro ao carregar ou processar o arquivo CSV: {e}")
        return None

# --- Endpoints Obrigatórios (Implementados anteriormente) ---

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Verifica a saúde da API.
    ---
    tags:
      - Health
    responses:
      200:
        description: A API está operacional.
    """
    return jsonify({"status": "healthy", "message": "API está operacional."}), 200

@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    """
    Lista todos os livros disponíveis na base de dados.
    ---
    tags:
      - Livros
    responses:
      200:
        description: Uma lista de todos os livros.
      503:
        description: Erro ao carregar a base de dados.
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada ou indisponível."}), 503
    return jsonify(df_books.to_dict(orient='records')), 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Retorna detalhes completos de um livro específico pelo ID.
    ---
    tags:
      - Livros
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: O ID único do livro.
    responses:
      200:
        description: Detalhes do livro solicitado.
      404:
        description: Livro não encontrado.
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
    book = df_books[df_books['id'] == book_id]
    if book.empty:
        return jsonify({"error": f"Livro com ID {book_id} não encontrado."}), 404
    return jsonify(book.to_dict(orient='records')[0]), 200

@app.route('/api/v1/books/search', methods=['GET'])
def search_books():
    """
    Busca livros por título e/ou categoria.
    ---
    tags:
      - Livros
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Parte do título do livro.
      - name: category
        in: query
        type: string
        required: false
        description: Categoria do livro.
    responses:
      200:
        description: Uma lista de livros que correspondem aos critérios.
      400:
        description: Nenhum parâmetro de busca fornecido.
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
    
    query_title = request.args.get('title')
    query_category = request.args.get('category')
    
    if not query_title and not query_category:
        return jsonify({"error": "Forneça 'title' ou 'category' como parâmetro."}), 400
        
    results = df_books.copy()
    if query_title:
        results = results[results['title'].str.contains(query_title, case=False, na=False)]
    if query_category:
        results = results[results['category'].str.contains(query_category, case=False, na=False)]
        
    if results.empty:
        return jsonify({"message": "Nenhum livro encontrado."}), 404
    return jsonify(results.to_dict(orient='records')), 200

@app.route('/api/v1/categories', methods=['GET'])
def get_all_categories():
    """
    Lista todas as categorias de livros disponíveis.
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Uma lista de todas as categorias únicas.
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
    unique_categories = df_books['category'].unique().tolist()
    return jsonify({"categories": unique_categories}), 200

# --- Endpoints Opcionais (Bônus) ---

@app.route('/api/v1/stats/overview', methods=['GET'])
def get_stats_overview():
    """
    Retorna estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings).
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Estatísticas gerais da coleção.
        schema:
          type: object
          properties:
            total_books:
              type: integer
              example: 1000
            average_price:
              type: number
              example: 35.07
            rating_distribution:
              type: object
              example: {"1": 200, "2": 196, "3": 203, "4": 197, "5": 204}
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
        
    try:
        total_books = int(len(df_books))
        average_price = round(df_books['price_numeric'].mean(), 2)
        
        # Conta a ocorrência de cada avaliação (1 a 5)
        rating_dist = df_books['rating_numeric'].value_counts().sort_index()
        # Converte para um formato JSON amigável
        rating_distribution = {str(k): int(v) for k, v in rating_dist.items()}
        
        return jsonify({
            "total_books": total_books,
            "average_price": average_price,
            "rating_distribution": rating_distribution
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao calcular estatísticas: {e}"}), 500

@app.route('/api/v1/stats/categories', methods=['GET'])
def get_stats_by_category():
    """
    Retorna estatísticas detalhadas por categoria (quantidade de livros, preços por categoria).
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Estatísticas agrupadas por categoria.
        schema:
          type: array
          items:
            type: object
            properties:
              category:
                type: string
              book_count:
                type: integer
              average_price:
                type: number
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
        
    try:
        # Agrupa por categoria e calcula a contagem e a média de preço
        stats = df_books.groupby('category').agg(
            book_count=('id', 'count'),
            average_price=('price_numeric', 'mean')
        ).reset_index()
        
        # Arredonda a média de preço
        stats['average_price'] = stats['average_price'].round(2)
        
        return jsonify(stats.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao calcular estatísticas por categoria: {e}"}), 500

@app.route('/api/v1/books/top-rated', methods=['GET'])
def get_top_rated_books():
    """
    Lista os livros com melhor avaliação (rating 5).
    ---
    tags:
      - Livros
    responses:
      200:
        description: Uma lista de livros com avaliação máxima (5 estrelas).
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503
        
    try:
        # Filtra livros onde 'rating_numeric' é 5
        top_rated_books = df_books[df_books['rating_numeric'] == 5]
        
        if top_rated_books.empty:
            return jsonify({"message": "Nenhum livro com 5 estrelas encontrado."}), 404
            
        return jsonify(top_rated_books.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar livros top-rated: {e}"}), 500

@app.route('/api/v1/books/price-range', methods=['GET'])
def get_books_by_price_range():
    """
    Filtra livros dentro de uma faixa de preço específica (min e/ou max).
    ---
    tags:
      - Livros
    parameters:
      - name: min
        in: query
        type: number
        format: float
        required: false
        description: O preço mínimo (inclusive).
      - name: max
        in: query
        type: number
        format: float
        required: false
        description: O preço máximo (inclusive).
    responses:
      200:
        description: Uma lista de livros dentro da faixa de preço.
      400:
        description: Parâmetros de preço inválidos.
    """
    df_books = load_books_data()
    if df_books is None:
        return jsonify({"error": "Base de dados não encontrada."}), 503

    # Pega 'min' e 'max' da URL, convertendo para float
    # Define padrões (0 para min, infinito para max) se não forem fornecidos
    try:
        min_price = request.args.get('min', default=0.0, type=float)
        max_price = request.args.get('max', default=np.inf, type=float)
    except ValueError:
        return jsonify({"error": "Parâmetros 'min' e 'max' devem ser números válidos."}), 400

    if min_price < 0 or max_price < 0:
        return jsonify({"error": "Preços não podem ser negativos."}), 400
        
    if min_price > max_price:
        return jsonify({"error": "O preço 'min' não pode ser maior que o 'max'."}), 400

    try:
        # Filtra o DataFrame
        results = df_books[
            (df_books['price_numeric'] >= min_price) &
            (df_books['price_numeric'] <= max_price)
        ]

        if results.empty:
            return jsonify({"message": "Nenhum livro encontrado nesta faixa de preço."}), 404
            
        return jsonify(results.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao filtrar por preço: {e}"}), 500

# --- Ponto de partida para executar a aplicação ---

if __name__ == '__main__':
    app.run()