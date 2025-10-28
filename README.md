# Tech Challenge - Fase 1: API Pública de Livros

Este projeto é o entregável principal da Fase 1 da Pós-Graduação em **Machine Learning Engineering**. O objetivo é demonstrar habilidades em engenharia de dados, desenvolvimento de API e deploy, criando um pipeline completo para consulta de livros.

O desafio consiste em desenvolver uma API pública para consulta de livros  começando pela extração dos dados (Web Scraping) de um site e terminando com o deploy da API em um ambiente de produção. Este README serve como documentação central do projeto.

---

## 🚀 Links Importantes

* **API em Produção (Vercel):** `https://postech-tech-challenge-f1.vercel.app/` 
* **Documentação (Swagger UI):** `https://postech-tech-challenge-f1.vercel.app/apidocs/` 
* **Vídeo de Apresentação:** `[COLOQUE_O_LINK_DO_VÍDEO_AQUI]` 

---

## 📐 Arquitetura do Projeto

O pipeline de dados deste projeto foi estruturado em três etapas principais:

1.  **Ingestão (Web Scraping):** Um script Python (`scripts/scrape_books.py`) foi desenvolvido para navegar pelo site `https://books.toscrape.com/`. Ele extrai informações detalhadas de todos os livros disponíveis (título, preço, rating, categoria, etc.)  e armazena esses dados localmente em um arquivo `data/books_data.csv`.
2.  **API RESTful (Flask):** Uma aplicação web utilizando **Flask**  (`api/app.py`) serve como o backend. Ela lê o arquivo `.csv` e disponibiliza os dados através de múltiplos endpoints JSON. A API também inclui documentação interativa **Swagger** (via Flasgger) para fácil consulta e teste
3.  **Deploy (Vercel):** A aplicação Flask foi configurada para ser hospedada na plataforma **Vercel**. O Vercel utiliza uma arquitetura *serverless*, onde a API é executada sob demanda. O arquivo `.csv` é comitado junto ao repositório e lido pela API em produção.

### Diagrama Visual

![Diagrama da Arquitetura](/docs/arquitetura_tech_challenge_f1.png)

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Web Scraping:** `requests` e `BeautifulSoup4`
* **Manipulação de Dados:** `Pandas` e `Numpy`
* **Framework da API:** `Flask` 
* **Documentação da API:** `Flasgger` (Swagger) 
* **Plataforma de Deploy:** `Vercel` 

---

## ⚙️ Instalação e Execução Local

Para reproduzir este projeto em sua máquina local, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/oDomLuiz/postech-tech-challenge-f1.git](https://github.com/oDomLuiz/postech-tech-challenge-f1.git)
    cd postech-tech-challenge-f1
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Web Scraping (Passo Obrigatório):**
    O script irá criar o arquivo `data/books_data.csv` que a API precisa para funcionar.
    ```bash
    python scripts/scrape_books.py
    ```

5.  **Inicie o servidor da API:**
    ```bash
    python api/app.py
    ```

O servidor estará rodando em `http://127.0.0.1:5000`. Você pode acessar a documentação do Swagger em `http://127.0.0.1:5000/apidocs`.

---

## 📚 Documentação da API (Endpoints) 

A API foi estruturada com a URL base `/api/v1`.

### Endpoints Obrigatórios 

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/health` | Verifica o status da API e a conectividade com os dados.  |
| `GET` | `/books` | Lista todos os livros disponíveis na base de dados.  |
| `GET` | `/books/{id}` | Retorna detalhes completos de um livro específico pelo ID.  |
| `GET` | `/books/search` | Busca livros por `title` (título) e/ou `category` (categoria).  |
| `GET` | `/categories` | Lista todas as categorias de livros únicas disponíveis.  |

### Endpoints Opcionais (Insights) 

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/stats/overview` | Retorna estatísticas gerais: total de livros, preço médio e distribuição de ratings.  |
| `GET` | `/stats/categories` | Retorna estatísticas detalhadas por categoria (contagem de livros, preço médio).  |
| `GET` | `/books/top-rated` | Lista os livros com a melhor avaliação (5 estrelas).  |
| `GET` | `/books/price-range` | Filtra livros dentro de uma faixa de preço (`min` e/ou `max`).  |

---

## 💡 Exemplos de Chamadas (Request/Response) 

Use a URL base do seu deploy (ou `http://127.0.0.1:5000`) para fazer as chamadas.

### Exemplo 1: Verificar a saúde da API

**Request:**
`GET /api/v1/health`

**Response (Exemplo):**
```json
{
    "message": "API está operacional.",
    "status": "healthy"
}
```

### Exemplo 2: Listar todos os livros da biblioteca

**Request:**
`GET /api/v1/books`

**Response (Exemplo):**
```json
[
    {
        "availability": "In stock (22 available)",
        "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "category": "Poetry",
        "id": 0,
        "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg",
        "price": "£51.77",
        "price_numeric": 51.77,
        "rating": "Three de 5 estrelas",
        "rating_numeric": 3,
        "title": "A Light in the Attic"
    },
  ...
]
```

### Exemplo 3: Listar todas as categorias de livros da biblioteca

**Request:**
`GET /api/v1/categories`

**Response (Exemplo):**
```json
{
    "categories": [
        "Poetry",
        "Historical Fiction",
        "Fiction",
        "Mystery",
        "History",
        "Young Adult",
        "Business",
        "Default",
        "Sequential Art",
        "Music",
        "Science Fiction",
        "Politics",
        "Travel",
        "Thriller",
        "Food and Drink",
        "Romance",
        "Childrens",
        "Art",
        "Spirituality",
        "Nonfiction",
        "Philosophy",
        "New Adult",
        "Contemporary",
        "Fantasy",
        "Add a comment",
        "Science",
        "Health",
        "Horror",
        "Self Help",
        "Religion",
        "Christian",
        "Crime",
        "Autobiography",
        "Christian Fiction",
        "Biography",
        "Womens Fiction",
        "Erotica",
        "Cultural",
        "Psychology",
        "Humor",
        "Historical",
        "Novels",
        "Short Stories",
        "Suspense",
        "Classics",
        "Academic",
        "Sports and Games",
        "Adult Fiction",
        "Parenting",
        "Paranormal"
    ]
}
```

### Exemplo 4: Buscar livros por títlo e/ou categoria (título poetry e categoria poetry)

**Request:**
`GET /api/v1/books/search?title=poetry&category=poetry`

**Response (Exemplo):**
```json
[
    {
        "availability": "In stock (14 available)",
        "book_url": "https://books.toscrape.com/catalogue/quarter-life-poetry-poems-for-the-young-broke-and-hangry_727/index.html",
        "category": "Poetry",
        "id": 271,
        "image_url": "https://books.toscrape.com/media/cache/68/92/68922093080c377fa521ba64d8d372e1.jpg",
        "price": "£50.89",
        "price_numeric": 50.89,
        "rating": "Five de 5 estrelas",
        "rating_numeric": 5,
        "title": "Quarter Life Poetry: Poems for the Young, Broke and Hangry"
    },
  ...
]
```

### Exemplo 5: Buscar livro por ID (ID 50)

**Request:**
`GET /api/v1/books/{{id}}`

**Response (Exemplo):**
```json
{
    "availability": "In stock (16 available)",
    "book_url": "https://books.toscrape.com/catalogue/throwing-rocks-at-the-google-bus-how-growth-became-the-enemy-of-prosperity_948/index.html",
    "category": "Nonfiction",
    "id": 50,
    "image_url": "https://books.toscrape.com/media/cache/f4/21/f4210912ca58ef35f8ad120fe3dfed38.jpg",
    "price": "£31.12",
    "price_numeric": 31.12,
    "rating": "Three de 5 estrelas",
    "rating_numeric": 3,
    "title": "Throwing Rocks at the Google Bus: How Growth Became the Enemy of Prosperity"
}
```

### Exemplo 6: Buscar livros entre uma faixa de valores (mínimo 10 e máximo 15)

**Request:**
`GET /api/v1/books/price-range?min=10&max=15`

**Response (Exemplo):**
```json
[
    {
        "availability": "In stock (19 available)",
        "book_url": "https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html",
        "category": "Default",
        "id": 10,
        "image_url": "https://books.toscrape.com/media/cache/a0/7e/a07ed8f1c23f7b4baf7102722680bd30.jpg",
        "price": "£13.99",
        "price_numeric": 13.99,
        "rating": "Two de 5 estrelas",
        "rating_numeric": 2,
        "title": "Starving Hearts (Triangular Trade Trilogy, #1)"
    },
  ...
]
```

### Exemplo 7: Buscar livros com avaliação 5 estrelas

**Request:**
`GET /api/v1/books/top-rated`

**Response (Exemplo):**
```json
[
    {
        "availability": "In stock (20 available)",
        "book_url": "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
        "category": "History",
        "id": 4,
        "image_url": "https://books.toscrape.com/media/cache/ce/5f/ce5f052c65cc963cf4422be096e915c9.jpg",
        "price": "£54.23",
        "price_numeric": 54.23,
        "rating": "Five de 5 estrelas",
        "rating_numeric": 5,
        "title": "Sapiens: A Brief History of Humankind"
    },
  ...
]
```

### Exemplo 8: Estatística dos livros por categorias

**Request:**
`GET /api/v1/stats/categories`

**Response (Exemplo):**
```json
[
    {
        "average_price": 13.12,
        "book_count": 1,
        "category": "Academic"
    },
  ...
]
```

### Exemplo 9: Estatística geral dos livros

**Request:**
`GET /api/v1/stats/overview`

**Response (Exemplo):**
```json
{
    "average_price": 35.08,
    "rating_distribution": {
        "1": 226,
        "2": 196,
        "3": 202,
        "4": 179,
        "5": 195
    },
    "total_books": 998
}
```
