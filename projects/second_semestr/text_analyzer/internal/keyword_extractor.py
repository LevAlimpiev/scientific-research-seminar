from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self):
        logger.info("Начинаем загрузку модели rubert-tiny2...")
        # Инициализируем модель для русского языка
        self.model = SentenceTransformer('cointegrated/rubert-tiny2')
        logger.info("Модель rubert-tiny2 успешно загружена!")

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Извлекает ключевые слова из текста используя sentence-transformers
        :param text: Исходный текст
        :param top_n: Количество ключевых слов для извлечения
        :return: Список кортежей (ключевое слово, оценка)
        """
        if not text:
            return []
            
        # Разбиваем текст на слова, удаляя пунктуацию
        words = re.findall(r'\w+', text, flags=re.UNICODE)
        
        # Удаляем дубликаты, сохраняя порядок
        unique_words = []
        seen = set()
        for word in words:
            if word.lower() not in seen and len(word) > 2:  # игнорируем короткие слова
                seen.add(word.lower())
                unique_words.append(word)
                
        if not unique_words:
            return []
            
        logger.info(f"Начинаем обработку текста из {len(unique_words)} уникальных слов...")
        
        # Разбиваем текст на предложения
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Обрабатываем предложения по частям
        batch_size = 32
        sentence_embeddings = []
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            logger.info(f"Обрабатываем пакет предложений {i+1}-{min(i+batch_size, len(sentences))} из {len(sentences)}")
            batch_embeddings = self.model.encode(batch)
            sentence_embeddings.extend(batch_embeddings)
        sentence_embeddings = np.array(sentence_embeddings)
        
        # Обрабатываем слова по частям
        word_embeddings = []
        for i in range(0, len(unique_words), batch_size):
            batch = unique_words[i:i + batch_size]
            logger.info(f"Обрабатываем пакет слов {i+1}-{min(i+batch_size, len(unique_words))} из {len(unique_words)}")
            batch_embeddings = self.model.encode(batch)
            word_embeddings.extend(batch_embeddings)
        word_embeddings = np.array(word_embeddings)
        
        # Вычисляем косинусное сходство между каждым словом и каждым предложением
        similarities = np.zeros(len(unique_words))
        for i, word_emb in enumerate(word_embeddings):
            # Находим максимальное сходство слова с любым предложением
            word_similarities = cosine_similarity([word_emb], sentence_embeddings)[0]
            similarities[i] = np.max(word_similarities)
        
        # Создаем список кортежей (слово, оценка)
        # Оценку переводим в 0-100 и берем только >=0
        keywords = [(word, int(max(0, score * 100))) for word, score in zip(unique_words, similarities)]
        
        # Сортируем по убыванию оценки
        keywords.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Извлечено {len(keywords[:top_n])} ключевых слов")
        return keywords[:top_n]
