from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Article, Keyword
from config.config import get_settings
from typing import List, Dict, Any

settings = get_settings()

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_article(db, article_id: int, title: str, content: str, keywords: List[Dict[str, Any]]) -> None:
    """Сохраняет статью и её ключевые слова в базу данных"""
    try:
        # Создаем новую статью
        article = Article(
            id=article_id,  # Используем article_id как id
            article_id=article_id,  # Добавляем article_id
            title=title,
            content=content
        )
        db.add(article)
        db.flush()  # Получаем id статьи
        
        # Добавляем ключевые слова
        for keyword in keywords:
            keyword_obj = Keyword(
                article_id=article.id,  # Используем id статьи
                keyword=keyword["keyword"],
                score=keyword["score"]
            )
            db.add(keyword_obj)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
