import os
import json
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL для доступа к сервисам
TEXT_ANALYZER_URL = "http://localhost:8001"  # сервис анализа текста

# Путь к HTML файлу роадмапа
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
ROADMAP_HTML_PATH = os.path.join(FRONTEND_PATH, 'index.html')

class KeywordMatcher:
    def __init__(self):
        self.roadmap_topics = {}
        self.roadmap_keywords = {}
        self.articles = {}
        self.article_keywords = {}
        
    def extract_topics_from_html(self):
        """Извлекает темы и подтемы из HTML файла роадмапа"""
        logger.info(f"Извлечение тем из файла {ROADMAP_HTML_PATH}")
        
        try:
            with open(ROADMAP_HTML_PATH, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Находим все секции с этапами (stage)
            stages = soup.find_all('div', class_='stage')
            
            for stage in stages:
                stage_id = stage.get('id', '')
                stage_title = stage.find('h3').text.strip() if stage.find('h3') else ''
                
                # Извлекаем все подтемы
                subtopics = []
                ul_element = stage.find('ul')
                if ul_element:
                    for li in ul_element.find_all('li', recursive=False):
                        subtopic_text = li.text.strip()
                        subtopics.append(subtopic_text)
                
                # Добавляем тему и подтемы в словарь
                self.roadmap_topics[stage_id] = {
                    'title': stage_title,
                    'subtopics': subtopics
                }
                
                # Извлекаем ключевые слова из заголовка и подтем
                keywords = self._extract_keywords_from_text(stage_title)
                for subtopic in subtopics:
                    keywords.extend(self._extract_keywords_from_text(subtopic))
                
                # Удаляем дубликаты и сохраняем ключевые слова для темы
                self.roadmap_keywords[stage_id] = list(set(keywords))
                
            logger.info(f"Извлечено {len(self.roadmap_topics)} тем из роадмапа")
            return self.roadmap_topics
                
        except Exception as e:
            logger.error(f"Ошибка при извлечении тем из HTML: {str(e)}")
            return {}
    
    def _extract_keywords_from_text(self, text):
        """Извлекает ключевые слова из текста"""
        # Удаляем скобки и их содержимое
        text = re.sub(r'\([^)]*\)', '', text)
        
        # Удаляем знаки препинания
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Разбиваем на слова
        words = [word.lower() for word in text.split() if len(word) > 3]
        
        # Фильтруем стоп-слова (можно расширить)
        stop_words = ['для', 'этой', 'его', 'она', 'они', 'это', 'или']
        filtered_words = [word for word in words if word not in stop_words]
        
        return filtered_words
    
    def create_mock_article(self):
        """Создаёт мок-статью через text_analyzer сервис"""
        try:
            url = f"{TEXT_ANALYZER_URL}/mock-article"
            response = requests.post(url)
            if response.status_code == 200:
                data = response.json()
                article_id = data.get('article_id', 1)
                logger.info(f"Создана мок-статья с ID {article_id}")
                
                # Сохраняем статью в локальные данные
                self.articles[article_id] = {
                    'id': article_id,
                    'name': data.get('title', ''),
                    'text': data.get('content', '')
                }
                self.article_keywords[article_id] = data.get('keywords', [])
                
                return True
            else:
                logger.error(f"Ошибка при создании мок-статьи: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при запросе к text_analyzer для создания мок-статьи: {str(e)}")
            return False
    
    def get_all_articles(self):
        """Получает все статьи из text_analyzer"""
        try:
            url = f"{TEXT_ANALYZER_URL}/articles"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                logger.info(f"Получено {len(articles)} статей из text_analyzer")
                
                # Сохраняем статьи и их ключевые слова
                for article in articles:
                    article_id = article.get('id')
                    self.articles[article_id] = {
                        'id': article_id,
                        'name': article.get('title', ''),
                        'text': article.get('content', '')
                    }
                    self.article_keywords[article_id] = article.get('keywords', [])
                    
                return articles
            else:
                logger.error(f"Ошибка при получении статей: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Ошибка при запросе к text_analyzer для получения статей: {str(e)}")
            return []
    
    def find_article_by_keywords(self, topic_keywords):
        """Находит статью, соответствующую ключевым словам темы"""
        if not self.article_keywords:
            # Если статьи еще не загружены, получаем их
            self.get_all_articles()
        
        if not self.article_keywords:
            logger.warning("Не удалось загрузить статьи для сопоставления")
            return None
        
        # Словарь для хранения оценок соответствия {article_id: score}
        article_scores = {}
        
        for article_id, keywords in self.article_keywords.items():
            # Преобразуем ключевые слова в нижний регистр для сравнения
            article_kw = [item['keyword'].lower() for item in keywords]
            
            # Считаем количество совпадающих ключевых слов
            matching_keywords = set(article_kw).intersection(set(topic_keywords))
            if matching_keywords:
                score = len(matching_keywords)
                article_scores[article_id] = score
        
        # Если найдены соответствия, возвращаем ID статьи с наибольшим соответствием
        if article_scores:
            best_article_id = max(article_scores, key=article_scores.get)
            logger.info(f"Найдена лучшая статья с ID {best_article_id} (оценка: {article_scores[best_article_id]})")
            return best_article_id
        
        return None
    
    def match_article_to_topics(self, article_id=None):
        """
        Сопоставляет статью с темами на основе ключевых слов.
        Если article_id не указан, находит лучшую статью для каждой темы.
        """
        # Если не указан конкретный ID статьи, работаем со всеми статьями
        if article_id is None:
            # Создаем мок-статью и получаем все статьи
            self.create_mock_article()
            all_articles = self.get_all_articles()
            
            # Результаты сопоставления {stage_id: {article_id, score, matching_keywords}}
            all_matches = {}
            
            # Для каждой темы находим наиболее подходящую статью
            for stage_id, keywords in self.roadmap_keywords.items():
                best_article_id = self.find_article_by_keywords(keywords)
                
                if best_article_id is not None and best_article_id in self.article_keywords:
                    article_kw = [item['keyword'].lower() for item in self.article_keywords[best_article_id]]
                    
                    # Количество совпадающих ключевых слов
                    matching_keywords = set(article_kw).intersection(set(keywords))
                    if matching_keywords:
                        # Оценка - количество совпадающих ключевых слов
                        score = len(matching_keywords)
                        all_matches[stage_id] = {
                            'article_id': best_article_id,
                            'score': score,
                            'matching_keywords': list(matching_keywords)
                        }
            
            return all_matches
        
        # Если указан конкретный ID статьи
        else:
            # Проверяем, есть ли статья в нашем кеше
            if article_id not in self.article_keywords:
                # Сначала пробуем получить все статьи
                self.get_all_articles()
                
                # Если после этого статья всё ещё не найдена, ничего не возвращаем
                if article_id not in self.article_keywords:
                    logger.warning(f"Статья с ID {article_id} не найдена")
                    return {}
            
            article_kw = [item['keyword'].lower() for item in self.article_keywords[article_id]]
            
            # Результаты сопоставления {stage_id: score}
            matches = {}
            
            for stage_id, keywords in self.roadmap_keywords.items():
                # Количество совпадающих ключевых слов
                matching_keywords = set(article_kw).intersection(set(keywords))
                if matching_keywords:
                    # Оценка - количество совпадающих ключевых слов
                    score = len(matching_keywords)
                    matches[stage_id] = {
                        'score': score,
                        'matching_keywords': list(matching_keywords)
                    }
            
            # Сортируем по убыванию оценки
            sorted_matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1]['score'], reverse=True)}
            
            return sorted_matches
    
    def update_html_with_article_links(self, matches):
        """Обновляет HTML файл, добавляя ссылки на статьи"""
        if not matches or not self.articles:
            logger.warning("Нет сопоставлений для обновления HTML")
            return False
        
        try:
            with open(ROADMAP_HTML_PATH, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            dom = etree.HTML(html_content)
            
            for stage_id, match_data in matches.items():
                article_id = match_data.get('article_id')
                if not article_id and 'score' in match_data:
                    # Это формат старого метода, используем текущий article_id
                    article_id = list(self.articles.keys())[0] if self.articles else None
                
                if article_id and article_id in self.articles:
                    article = self.articles[article_id]
                    
                    # Находим элемент ресурсов для этой темы
                    resources_ul = dom.xpath(f'//div[@id="{stage_id}"]/div[@class="stage-content"]/div[@class="resources"]/ul')
                    
                    if resources_ul:
                        # Создаем новый элемент li с ссылкой на статью
                        new_li = etree.Element("li")
                        new_a = etree.SubElement(new_li, "a")
                        new_a.set("href", f"#article-{article_id}")
                        new_a.set("class", "article-link")
                        new_a.set("data-article-id", str(article_id))
                        
                        score = match_data.get('score', 0)
                        new_a.text = f"{article.get('name', 'Статья')} (совпадение: {score})"
                        
                        # Добавляем новый элемент в ul
                        resources_ul[0].append(new_li)
                        
                        logger.info(f"Добавлена ссылка на статью {article_id} в тему {stage_id}")
            
            # Сохраняем обновленный HTML
            with open(ROADMAP_HTML_PATH, 'w', encoding='utf-8') as file:
                file.write(etree.tostring(dom, pretty_print=True, method="html", encoding='unicode'))
            
            logger.info(f"HTML файл успешно обновлен: {ROADMAP_HTML_PATH}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении HTML: {str(e)}")
            return False

# Пример использования
if __name__ == "__main__":
    matcher = KeywordMatcher()
    
    # Извлекаем темы из HTML
    matcher.extract_topics_from_html()
    
    # Создаем мок-статью и получаем все статьи
    matcher.create_mock_article()
    matcher.get_all_articles()
    
    # Сопоставляем статьи с темами без указания конкретной статьи
    matches = matcher.match_article_to_topics()
    logger.info(f"Сопоставления для всех статей: {json.dumps(matches, indent=2)}")
    
    # Обновляем HTML
    matcher.update_html_with_article_links(matches) 