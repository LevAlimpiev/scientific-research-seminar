import requests
from config.config import get_settings

settings = get_settings()

class ScrapperClient:
    def __init__(self):
        self.base_url = settings.SCRAPPER_SERVICE_URL
    
    def get_article(self, article_id: int) -> dict:
        """
        Получает статью из сервиса scrapper
        :param article_id: ID статьи
        :return: Данные статьи
        """
        response = requests.get(f"{self.base_url}/api/v1/scrapping/article/{article_id}")
        response.raise_for_status()
        return response.json() 