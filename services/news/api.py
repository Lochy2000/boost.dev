import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class NewsAPIService:
    """
    Service for interacting with the News API.
    Handles fetching tech news articles with proper caching and error handling.
    """
    BASE_URL = "https://newsapi.org/v2"
    CACHE_TTL = 60 * 30  # Cache for 30 minutes
    
    def __init__(self, api_key=None):
        """Initialize the service with an API key."""
        self.api_key = api_key or settings.NEWS_API_KEY
        
    def get_tech_news(self, page=1, page_size=12, category="technology"):
        """
        Fetch technology news articles.
        
        Args:
            page (int): Page number for pagination
            page_size (int): Number of articles per page
            category (str): News category (default: technology)
            
        Returns:
            dict: API response with articles and metadata
        """
        cache_key = f"tech_news_{category}_{page}_{page_size}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info("Returning cached tech news")
            return cached_data
        
        # Calculate date for 'from' parameter (last 7 days)
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        params = {
            'apiKey': self.api_key,
            'category': category,
            'language': 'en',
            'page': page,
            'pageSize': page_size,
            'from': from_date,
            'sortBy': 'publishedAt'
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/top-headlines", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Store in cache
            cache.set(cache_key, data, self.CACHE_TTL)
            logger.info(f"Fetched {len(data.get('articles', []))} tech news articles")
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tech news: {str(e)}")
            # Return empty results structure on error
            return {
                'status': 'error',
                'articles': [],
                'totalResults': 0,
                'message': f"Error fetching articles: {str(e)}"
            }
    
    def search_tech_news(self, query, page=1, page_size=12):
        """
        Search for tech news articles by keyword.
        
        Args:
            query (str): Search term
            page (int): Page number for pagination
            page_size (int): Number of articles per page
            
        Returns:
            dict: API response with articles and metadata
        """
        cache_key = f"tech_news_search_{query}_{page}_{page_size}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached search results for '{query}'")
            return cached_data
        
        # Calculate date for 'from' parameter (last 30 days)
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        params = {
            'apiKey': self.api_key,
            'q': f"{query} AND technology",
            'language': 'en',
            'page': page,
            'pageSize': page_size,
            'from': from_date,
            'sortBy': 'relevancy'
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/everything", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Store in cache
            cache.set(cache_key, data, self.CACHE_TTL)
            logger.info(f"Fetched {len(data.get('articles', []))} articles for search '{query}'")
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching tech news: {str(e)}")
            # Return empty results structure on error
            return {
                'status': 'error',
                'articles': [],
                'totalResults': 0,
                'message': f"Error searching articles: {str(e)}"
            }


# Helper function to get a singleton instance of the service
def get_news_service():
    """
    Get a configured NewsAPIService instance.
    
    Returns:
        NewsAPIService: Configured service instance
    """
    return NewsAPIService()
