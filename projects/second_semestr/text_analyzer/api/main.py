from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
import logging
import requests
import httpx
from fastapi.middleware.cors import CORSMiddleware

from internal.database import get_db, init_db, save_article, SessionLocal, get_all_articles
from internal.keyword_extractor import KeywordExtractor
from internal.scrapper_client import ScrapperClient
from config.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text Analyzer Service")
settings = get_settings()
keyword_extractor = KeywordExtractor()
scrapper_client = ScrapperClient()
# Инициализируем базу данных напрямую, а не как генератор
db = SessionLocal()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordResponse(BaseModel):
    keyword: str
    score: int

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    keywords: List[KeywordResponse]

class MockArticleRequest(BaseModel):
    topic: str = "Многопоточное программирование"  # Опциональная тема для генерации статьи по C++, значение по умолчанию
    
    class Config:
        # Разрешаем создание модели с пустыми значениями
        validate_assignment = True
        extra = "ignore"

@app.on_event("startup")
async def startup_event():
    logger.info("Инициализация базы данных...")
    init_db()
    logger.info("База данных инициализирована")

@app.get("/analyze/{article_id}")
async def analyze_article(article_id: int) -> Dict[str, Any]:
    try:
        logger.info(f"Начинаем анализ статьи {article_id}")
        
        # Получаем статью из scrapper
        async with httpx.AsyncClient() as client:
            logger.info(f"Запрашиваем статью из scrapper: {settings.SCRAPPER_SERVICE_URL}/api/v1/scrapping/article/{article_id}")
            response = await client.get(f"{settings.SCRAPPER_SERVICE_URL}/api/v1/scrapping/article/{article_id}")
            response.raise_for_status()
            article_data = response.json()
            logger.info(f"Получена статья: {article_data['name']}")

        # Обрезаем текст до 200 символов для быстрого анализа (не хватает выч. ресурсов)
        truncated_text = article_data["text"][:200]
        logger.info(f"Обрабатываем первые 200 символов статьи: '{truncated_text}'")

        # Извлекаем ключевые слова
        logger.info("Начинаем извлечение ключевых слов")
        keywords_tuples = keyword_extractor.extract_keywords(truncated_text)
        keywords = [{"keyword": word, "score": score} for word, score in keywords_tuples]
        logger.info(f"Извлечено {len(keywords)} ключевых слов")

        # Сохраняем статью и ключевые слова в базу данных
        try:
            logger.info("Сохраняем статью в базу данных")
            save_article(
                db=db,
                article_id=article_id,
                title=article_data["name"],
                content=truncated_text,  # Сохраняем только обрезанный текст
                keywords=keywords
            )
            logger.info("Статья успешно сохранена")
        except Exception as e:
            if "duplicate key value violates unique constraint" in str(e):
                logger.info("Статья уже существует в базе данных")
            else:
                logger.error(f"Ошибка при сохранении статьи: {str(e)}")
                raise

        return {
            "status": "success",
            "article_id": article_id,
            "title": article_data["name"],
            "keywords": keywords
        }

    except httpx.HTTPError as e:
        logger.error(f"Ошибка при получении статьи: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статьи: {str(e)}")

@app.post("/mock-article")
@app.get("/mock-article")
async def create_mock_article() -> Dict[str, Any]:
    """
    Генерирует короткую мок-статью по C++ без обращения к базе данных.
    Просто возвращает захардкоженные данные.
    """
    # Хардкодим все данные
    topic = "Многопоточное программирование"
    title = f"C++: {topic}"
    content = """C++ предоставляет мощные инструменты для разработки многопоточных приложений.
Стандартная библиотека C++11 и выше включает классы std::thread, std::mutex, std::condition_variable 
и другие примитивы синхронизации, которые позволяют эффективно создавать параллельные программы."""
    
    # Захардкоженные ключевые слова
    keywords = [
        {"keyword": "C++", "score": 10},
        {"keyword": "многопоточность", "score": 8},
        {"keyword": "std::thread", "score": 7},
        {"keyword": "std::mutex", "score": 6},
        {"keyword": "синхронизация", "score": 5}
    ]
    
    return {
        "status": "success",
        "article_id": 1,
        "title": title,
        "content": content,
        "keywords": keywords
    }

@app.get("/articles")
async def get_articles() -> Dict[str, Any]:
    """
    Возвращает все статьи из базы данных
    """
    try:
        logger.info("Получение всех статей из базы данных")
        
        # Получаем все статьи из базы данных
        articles = get_all_articles(db)
        
        # Формируем ответ
        result = []
        for article in articles:
            article_data = {
                "id": article.article_id,
                "title": article.title,
                "content": article.content,
                "keywords": [
                    {"keyword": kw.keyword, "score": kw.score}
                    for kw in article.keywords
                ]
            }
            result.append(article_data)
        
        logger.info(f"Получено {len(result)} статей из базы данных")
        
        return {
            "status": "success",
            "count": len(result),
            "articles": result
        }
    
    except Exception as e:
        logger.error(f"Ошибка при получении статей: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статей: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    ) 