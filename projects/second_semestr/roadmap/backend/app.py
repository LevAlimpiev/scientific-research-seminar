from flask import Flask, send_from_directory, jsonify, request
import os
import sys
from keyword_matcher_new import KeywordMatcher

app = Flask(__name__)

# Корневой путь к статическим файлам фронтенда
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

# Создаем экземпляр KeywordMatcher
matcher = KeywordMatcher()

@app.route('/')
def index():
    """Обслуживание главной страницы"""
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Обслуживание других статических файлов"""
    if os.path.exists(os.path.join(FRONTEND_PATH, path)):
        return send_from_directory(FRONTEND_PATH, path)
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/api/extract-topics', methods=['GET'])
def extract_topics():
    """Извлекает темы из HTML файла роадмапа"""
    topics = matcher.extract_topics_from_html()
    return jsonify({
        "status": "success",
        "topics_count": len(topics),
        "topics": topics
    })

@app.route('/api/match-article', methods=['POST'])
def match_article():
    """Сопоставляет статью с темами роадмапа"""
    data = request.json
    article_id = data.get('article_id')
    
    # Извлекаем темы, если еще не извлечены
    if not matcher.roadmap_topics:
        matcher.extract_topics_from_html()
    
    # Если ID статьи не указан, находим лучшие статьи для каждой темы
    if article_id is None:
        # Создаем мок-статью и получаем все статьи
        matcher.create_mock_article()
        matcher.get_all_articles()
        
        # Сопоставляем с темами
        matches = matcher.match_article_to_topics()
        
        return jsonify({
            "status": "success",
            "matches_count": len(matches),
            "matches": matches
        })
    else:
        # Получаем все статьи, чтобы найти нужную
        matcher.get_all_articles()
        
        # Сопоставляем с темами
        matches = matcher.match_article_to_topics(article_id)
        
        return jsonify({
            "status": "success",
            "article_id": article_id,
            "matches_count": len(matches),
            "matches": matches
        })

@app.route('/api/update-roadmap', methods=['POST'])
def update_roadmap():
    """Обновляет HTML роадмапа, добавляя ссылки на статьи"""
    data = request.json
    article_id = data.get('article_id')
    
    # Извлекаем темы, если еще не извлечены
    if not matcher.roadmap_topics:
        matcher.extract_topics_from_html()
    
    # Если ID статьи не указан, находим лучшие статьи для каждой темы
    if article_id is None:
        # Создаем мок-статью и получаем все статьи
        matcher.create_mock_article()
        matcher.get_all_articles()
        
        # Сопоставляем с темами без указания конкретной статьи
        matches = matcher.match_article_to_topics()
    else:
        # Получаем все статьи, чтобы найти нужную
        matcher.get_all_articles()
        
        # Сопоставляем конкретную статью с темами
        matches = matcher.match_article_to_topics(article_id)
    
    # Обновляем HTML
    success = matcher.update_html_with_article_links(matches)
    
    if success:
        return jsonify({
            "status": "success",
            "message": "Роадмап успешно обновлен",
            "matches_count": len(matches)
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Не удалось обновить роадмап"
        }), 500

if __name__ == '__main__':
    print(f"Сервер запущен. Откройте http://localhost:5000 в браузере.")
    app.run(debug=True, host='0.0.0.0', port=5000) 