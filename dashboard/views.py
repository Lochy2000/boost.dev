from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from services.weather import get_weather_service
from challenges.models import ChallengeSolution
from wins.models import DailyWin
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    """
    Main dashboard view showing user stats, upcoming challenges, and weather
    """
    user = request.user
    context = {
        'user': user,
    }
    
    # Get user stats
    solutions_count = ChallengeSolution.objects.filter(user=user).count()
    context['solutions_count'] = solutions_count
    
    # Get all challenge solutions for the Recent Challenge Solutions section
    all_challenge_solutions = ChallengeSolution.objects.select_related('user', 'challenge').order_by('-submitted_at')[:10]
    context['all_challenge_solutions'] = all_challenge_solutions
    
    # Get recommended challenges
    from challenges.models import Challenge
    recommended_challenges = Challenge.objects.all().order_by('?')[:3]
    context['recommended_challenges'] = recommended_challenges
    
    # Get public community wins
    community_wins = DailyWin.objects.filter(is_public=True).select_related('user').order_by('-created_at')[:5]
    context['community_wins'] = community_wins
    
    # Get wins data
    wins = DailyWin.objects.filter(user=user).order_by('-created_at')
    context['wins'] = wins
    context['wins_count'] = wins.count()
    
    # Get AI Boost for daily inspiration
    try:
        from services.ai_boost import get_daily_boost
        ai_boost = get_daily_boost(username=user.username)
        context['ai_boost'] = ai_boost
    except Exception as e:
        logger.error(f"Error getting AI boost: {e}")
        # Fallback boost
        context['ai_boost'] = {
            "quote": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "challenge": "Take 15 minutes today to work on a coding problem that excites you."
        }
    
    # Get weather data
    try:
        weather_service = get_weather_service()
        weather_data = weather_service.get_uk_weather()
        context['weather'] = weather_data
        logger.info(f"Weather data added to context: {weather_data}")
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        # Provide fallback weather data
        context['weather'] = {
            'city': 'London',
            'country': 'UK',
            'temperature': 18,
            'condition': 'Clouds',
            'description': 'scattered clouds',
            'icon': '03d'
        }
        
    # Get tech news for the dashboard
    try:
        from services.news.api import get_news_service
        news_service = get_news_service()
        news_results = news_service.get_tech_news(page=1, page_size=5)
        tech_news_items = news_results.get('articles', [])
        context['tech_news_items'] = tech_news_items
    except Exception as e:
        logger.error(f"Error fetching tech news for dashboard: {e}")
        context['tech_news_items'] = []
    
    # Get solutions by correctness level
    correct_solutions = ChallengeSolution.objects.filter(
        user=user, 
        correctness_level='correct'
    ).count()
    
    partial_solutions = ChallengeSolution.objects.filter(
        user=user, 
        correctness_level='partial'
    ).count()
    
    incorrect_solutions = ChallengeSolution.objects.filter(
        user=user, 
        correctness_level='incorrect'
    ).count()
    
    context['correct_solutions'] = correct_solutions
    context['partial_solutions'] = partial_solutions
    context['incorrect_solutions'] = incorrect_solutions
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def community(request):
    """Community view showing public wins and activity"""
    # Get public wins
    public_wins = DailyWin.objects.filter(is_public=True).order_by('-created_at')[:10]
    
    context = {
        'public_wins': public_wins,
    }
    
    return render(request, 'dashboard/community.html', context)

@login_required
def tech_news(request):
    """View for displaying technology news articles"""
    from services.news.api import get_news_service
    
    page = int(request.GET.get('page', 1))
    category = request.GET.get('category', 'technology')
    query = request.GET.get('q', '')
    
    # Map category slugs to actual News API categories
    category_mapping = {
        'technology': 'technology',
        'programming': 'technology',  # Use tech category + search filtering
        'ai': 'technology',  # Use tech category + search filtering
        'web': 'technology',  # Use tech category + search filtering
        'mobile': 'technology',  # Use tech category + search filtering
    }
    
    # Get appropriate API category
    api_category = category_mapping.get(category, 'technology')
    
    # Initialize the news service
    news_service = get_news_service()
    
    # Calculate pagination info
    items_per_page = 12  # This is our standard page size
    
    # Get articles based on whether we're searching or browsing
    if query:
        # Search mode
        search_term = query
        if category and category != 'technology':
            # Add category-specific terms to the search
            if category == 'programming':
                search_term += ' programming developer code'
            elif category == 'ai':
                search_term += ' artificial intelligence machine learning'
            elif category == 'web':
                search_term += ' web development javascript frontend backend'
            elif category == 'mobile':
                search_term += ' mobile app android ios'
        
        # Get search results
        results = news_service.search_tech_news(search_term, page=page, page_size=items_per_page)
    else:
        # Browse mode
        if category and category != 'technology':
            # For specialized categories, first get tech news then filter
            results = news_service.get_tech_news(page=page, category=api_category, page_size=items_per_page*3)  # Get more articles to filter from
            articles = results.get('articles', [])
            
            # Filter articles based on specialized category
            if category == 'programming':
                keywords = ['programming', 'developer', 'code', 'software', 'github', 'language', 'python', 'javascript', 'java']
            elif category == 'ai':
                keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'neural', 'deep learning', 'llm', 'gpt']
            elif category == 'web':
                keywords = ['web', 'website', 'frontend', 'backend', 'javascript', 'html', 'css', 'php', 'react', 'angular']
            elif category == 'mobile':
                keywords = ['mobile', 'app', 'android', 'ios', 'iphone', 'smartphone', 'tablet', 'apps']
            else:
                keywords = []
            
            # Filter articles that match any of the keywords
            if keywords:
                filtered_articles = []
                for article in articles:
                    title = (article.get('title', '') or '').lower()
                    description = (article.get('description', '') or '').lower()
                    content = (article.get('content', '') or '').lower()
                    combined_text = title + ' ' + description + ' ' + content
                    
                    if any(keyword.lower() in combined_text for keyword in keywords):
                        filtered_articles.append(article)
                
                # Update the results with filtered articles
                results['articles'] = filtered_articles[:items_per_page]  # Limit to original page_size
                results['totalResults'] = len(filtered_articles)
        else:
            # For generic technology category, use the API directly
            results = news_service.get_tech_news(page=page, category=api_category, page_size=items_per_page)
    
    # Process results
    articles = results.get('articles', [])
    total_results = results.get('totalResults', 0)
    error_message = results.get('message', None) if results.get('status') == 'error' else None
    
    # Calculate pagination info
    items_per_page = 12
    total_pages = (total_results + items_per_page - 1) // items_per_page
    has_next = page < total_pages
    has_prev = page > 1
    
    context = {
        'articles': articles,
        'total_results': total_results,
        'page': page,
        'total_pages': total_pages,
        'has_next': has_next,
        'has_prev': has_prev,
        'query': query,
        'category': category,
        'error_message': error_message,
    }
    
    return render(request, 'dashboard/tech_news.html', context)
