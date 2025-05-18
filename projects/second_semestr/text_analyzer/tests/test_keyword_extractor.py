import pytest
import sys
from internal.keyword_extractor import KeywordExtractor

# Выводим информацию перед импортом для отладки
print("========== НАЧАЛО ВЫПОЛНЕНИЯ ФАЙЛА ТЕСТОВ ==========")
print(f"Python версия: {sys.version}")
print(f"Путь к Python: {sys.executable}")

def test_extract_keywords():
    print("Начинаем тест extract_keywords...")
    
    # Очень короткий текст для тестирования
    text = "Python язык программирования."
    print(f"Тестовый текст: '{text}'")
    
    try:
        # Создаем реальный экземпляр KeywordExtractor
        print("Создаем реальный экземпляр KeywordExtractor...")
        extractor = KeywordExtractor()
        print("Экземпляр KeywordExtractor создан успешно")
        
        # Ограничиваем до 3 ключевых слов для уменьшения нагрузки
        print("Вызываем extract_keywords с top_n=3...")
        keywords = extractor.extract_keywords(text, top_n=3)
        print(f"Получены ключевые слова: {keywords}")
        
        # Проверяем базовую структуру результата
        print("Проверяем структуру результата...")
        assert isinstance(keywords, list), "Результат должен быть списком"
        assert len(keywords) > 0, "Список ключевых слов не должен быть пустым"
        assert all(isinstance(k[0], str) for k in keywords), "Первый элемент каждой пары должен быть строкой"
        assert all(isinstance(k[1], int) for k in keywords), "Второй элемент каждой пары должен быть целым числом"
        assert all(0 <= k[1] <= 100 for k in keywords), "Оценки должны быть в диапазоне 0-100"
        
        print("Все проверки пройдены успешно")
        
    except Exception as e:
        print(f"Ошибка в тесте: {e}")
        raise
