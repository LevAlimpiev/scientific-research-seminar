import pytest
from internal.keyword_extractor import KeywordExtractor

@pytest.fixture
def extractor():
    return KeywordExtractor()

def test_extract_keywords(extractor):
    text = "О, конечно, программирование на Python - это просто райское наслаждение! Особенно когда твой код работает с первого раза, а баги сами исправляются. А эти бесконечные обновления библиотек - просто мечта каждого разработчика!"
    
    keywords = extractor.extract_keywords(text)
    
    # Проверяем базовую структуру результата
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert all(isinstance(k[0], str) for k in keywords)
    assert all(isinstance(k[1], int) for k in keywords)
    assert all(0 <= k[1] <= 100 for k in keywords)  # Проверяем, что оценки в диапазоне 0-100
    
    # Проверяем, что "Python" присутствует в ключевых словах
    python_keywords = [k for k in keywords if "python" in k[0].lower()]
    assert len(python_keywords) > 0
    
    # Проверяем, что "программирование" присутствует в ключевых словах
    programming_keywords = [k for k in keywords if "программирование" in k[0].lower()]
    assert len(programming_keywords) > 0
