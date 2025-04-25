import requests
import logging
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service for interacting with OpenWeatherMap API.
    Fetches weather data for the UK with proper caching and error handling.
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    CACHE_TTL = 60 * 60  # Cache for 1 hour
    
    def __init__(self, api_key=None):
        """Initialize the service with an API key."""
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY') or getattr(settings, 'OPENWEATHER_API_KEY', None)
        
        # Force reload environment variables to ensure we get the latest API key
        if not self.api_key:
            load_dotenv(override=True)
            self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not found. Using mock data.")
        
    def get_uk_weather(self, city="London"):
        """
        Fetch current weather for a UK city.
        
        Args:
            city (str): UK city name (default: London)
            
        Returns:
            dict: Weather data including temperature, conditions, etc.
        """
        # Return mock data if no API key
        if not self.api_key:
            logger.warning("No API key available for weather service")
            return self._get_mock_weather(city)
            
        logger.info(f"Using API key: {self.api_key[:4]}...{self.api_key[-4:] if self.api_key else None}")
            
        cache_key = f"weather_{city.lower()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached weather for {city}")
            return cached_data
        
        params = {
            'appid': self.api_key,
            'q': f"{city},uk",
            'units': 'metric'  # Use metric units
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/weather", params=params)
            
            # Check for 401 errors specifically
            if response.status_code == 401:
                logger.error(f"API key unauthorized: {response.text}")
                print(f"API key {self.api_key} is unauthorized. This could be because:")
                print("1. The API key is new and not yet activated (may take a few hours)")
                print("2. The account has reached its quota")
                print("3. There's an issue with the account")
                return self._get_mock_weather(city, error=f"{response.status_code} {response.reason} for url: {response.url}")
                
            response.raise_for_status()
            data = response.json()
            
            # Process and format the data
            processed_data = {
                'city': city,
                'country': 'UK',
                'temperature': round(data.get('main', {}).get('temp', 0)),
                'feels_like': round(data.get('main', {}).get('feels_like', 0)),
                'humidity': data.get('main', {}).get('humidity', 0),
                'condition': data.get('weather', [{}])[0].get('main', 'Unknown'),
                'description': data.get('weather', [{}])[0].get('description', 'Unknown'),
                'icon': data.get('weather', [{}])[0].get('icon', ''),
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'timestamp': datetime.now().strftime('%B %d'),
            }
            
            # Store in cache
            cache.set(cache_key, processed_data, self.CACHE_TTL)
            logger.info(f"Fetched weather for {city}")
            
            return processed_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather for {city}: {str(e)}")
            # Return default data on error
            return self._get_mock_weather(city, error=str(e))
    
    def _get_mock_weather(self, city="London", error=None):
        """Return mock weather data for development/testing purposes"""
        import random
        
        # Get current time to determine appropriate weather
        current_hour = datetime.now().hour
        
        # Determine if it's day or night for icon selection
        time_of_day = 'd' if 6 <= current_hour < 20 else 'n'
        
        # Create realistic weather options based on season and location
        weather_options = [
            {'condition': 'Clear', 'description': 'clear sky', 'icon': f'01{time_of_day}', 'temp_range': (16, 25)},
            {'condition': 'Clouds', 'description': 'scattered clouds', 'icon': f'02{time_of_day}', 'temp_range': (14, 22)},
            {'condition': 'Clouds', 'description': 'broken clouds', 'icon': f'03{time_of_day}', 'temp_range': (13, 20)},
            {'condition': 'Clouds', 'description': 'overcast clouds', 'icon': f'04{time_of_day}', 'temp_range': (12, 19)},
            {'condition': 'Rain', 'description': 'light rain', 'icon': f'10{time_of_day}', 'temp_range': (10, 18)},
        ]
        
        # Choose a random weather condition
        weather = random.choice(weather_options)
        temperature = random.randint(*weather['temp_range'])
        feels_like = temperature - random.randint(0, 3)  # Usually feels slightly colder
        
        # Mock weather data for development
        mock_data = {
            'city': city,
            'country': 'UK',
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': random.randint(55, 90),
            'condition': weather['condition'],
            'description': weather['description'],
            'icon': weather['icon'],
            'wind_speed': round(random.uniform(2.0, 8.0), 1),
            'timestamp': datetime.now().strftime('%B %d'),
        }
        
        # Make sure the data meets essential requirements
        logger.info(f"Generated realistic mock weather data for {city}")
        
        # Add error message if provided
        if error:
            mock_data['error'] = f"Error fetching weather: {error}"
            logger.warning(f"Using mock data due to error: {error}")
            
        return mock_data

# Helper function to get a singleton instance of the service
def get_weather_service():
    """
    Get a configured WeatherService instance.
    
    Returns:
        WeatherService: Configured service instance
    """
    return WeatherService()
