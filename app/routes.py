from flask import Blueprint, request, jsonify
import jwt
import datetime
from werkzeug.security import check_password_hash
from .models import User
from . import db
import csv
from flask import current_app
import os

api_bp = Blueprint('api', __name__)

# SECRET_KEY = 'your-secret-key'  # Use uma variável de ambiente em produção!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')  # Preferencialmente defina no ambiente do Vercel

BOOKS_CSV_PATH = os.path.join(os.path.dirname(__file__), 'books.csv')

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password, data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@api_bp.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': f'Hello user {data["user_id"]}!'})
    except:
        return jsonify({'message': 'Token is invalid!'}), 403

def load_books():
    books = []
    try:
        with open(BOOKS_CSV_PATH, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                row['id'] = idx + 1  # Adiciona um ID incremental
                books.append(row)
    except Exception as e:
        current_app.logger.error(f"Erro ao carregar books.csv: {e}")
    return books

@api_bp.route('/api/v1/books', methods=['GET'])
def get_books():
    books = load_books()
    return jsonify(books), 200

@api_bp.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    books = load_books()
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({'message': 'Book not found'}), 404

@api_bp.route('/api/v1/books/search', methods=['GET'])
def search_books():
    title = request.args.get('title', '').lower()
    category = request.args.get('category', '').lower()
    books = load_books()
    filtered = []
    for book in books:
        matches_title = title in book['title'].lower() if title else True
        matches_category = category in book['category'].lower() if category else True
        if matches_title and matches_category:
            filtered.append(book)
    return jsonify(filtered), 200

@api_bp.route('/api/v1/categories', methods=['GET'])
def get_categories():
    books = load_books()
    categories = sorted(set(book['category'] for book in books if book['category']))
    return jsonify(categories), 200

@api_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    try:
        books = load_books()
        status = 'ok' if books else 'no data'
        return jsonify({'status': status, 'books_count': len(books)}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500
