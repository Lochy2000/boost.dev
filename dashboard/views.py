from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Article, Project, ProjectFeedback, Resource
from prompts.models import DailyPrompt
from wins.models import DailyWin
from challenges.models import Challenge, ChallengeSolution
from .forms import ProjectFeedbackForm
from services.news import get_news_service
import random

def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return render(request, 'home.html')

def dashboard(request):
    """User dashboard view"""
    # Get featured articles
    featured_articles = Article.objects.filter(is_featured=True)[:2]
    
    # Get recent articles
    recent_articles = Article.objects.filter(is_featured=False)[:4]
    
    # Get latest tech news from API for dashboard display
    tech_news_items = []
    try:
        news_service = get_news_service()
        news_data = news_service.get_tech_news(page=1, page_size=4)
        tech_news_items = news_data.get('articles', [])
    except Exception as e:
        # Log error but continue loading the page
        import logging
        logging.error(f"Error fetching tech news for dashboard: {str(e)}")
    
    
    # Get popular projects
    popular_projects = Project.objects.order_by('-stars')[:4]
    
    # Get featured resources
    featured_resources = Resource.objects.filter(is_featured=True)[:3]
    
    # Get today's prompt
    daily_prompt = DailyPrompt.get_today()
    
    # Get user's challenge stats and recent submissions
    user_challenge_count = 0
    user_challenge_solutions = []
    
    if request.user.is_authenticated:
        # Count user challenge solutions
        user_challenge_count = ChallengeSolution.objects.filter(user=request.user).count()
        
        # Get recent challenge solutions
        user_challenge_solutions = ChallengeSolution.objects.filter(
            user=request.user
        ).select_related('challenge').order_by('-submitted_at')[:3]
    
    # Get user's recent wins
    user_wins = []
    has_win_today = False
    
    if request.user.is_authenticated:
        user_wins = DailyWin.objects.filter(user=request.user).order_by('-created_at')[:3]
        
        # Check if user has a win for today
        today = timezone.now().date()
        has_win_today = DailyWin.objects.filter(
            user=request.user, 
            created_at__date=today
        ).exists()
    
    # Get community wins
    community_wins = DailyWin.objects.filter(is_public=True).exclude(user=request.user).order_by('-created_at')[:5]
    
    # Get recommended challenges
    recommended_challenges = Challenge.objects.filter(is_approved=True).order_by('?')[:3]
    
    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
        'popular_projects': popular_projects,
        'featured_resources': featured_resources,
        'daily_prompt': daily_prompt,
        'community_wins': community_wins,
        'user_wins': user_wins,
        'has_win_today': has_win_today,
        'user': request.user,
        'user_challenge_count': user_challenge_count,
        'user_challenge_solutions': user_challenge_solutions,
        'recommended_challenges': recommended_challenges,
        'tech_news_items': tech_news_items,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

def index(request):
    """Main dashboard view showing a grid of content cards"""
    # For now, just use the dashboard view
    return dashboard(request)

def article_list(request):
    """View for listing all articles with filtering"""
    # Get query parameters
    q = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    
    # Base queryset
    articles = Article.objects.all()
    
    # Apply search filter
    if q:
        articles = articles.filter(
            Q(title__icontains=q) | 
            Q(summary__icontains=q) | 
            Q(content__icontains=q) |
            Q(tags__icontains=q)
        )
    
    # Apply tag filter
    if tag:
        articles = articles.filter(tags__icontains=tag)
    
    # Get unique tags for filter sidebar
    all_tags = set()
    for article in Article.objects.all():
        for tag in article.get_tags_list():
            all_tags.add(tag)
    
    context = {
        'articles': articles,
        'query': q,
        'tag_filter': tag,
        'all_tags': sorted(all_tags),
    }
    
    return render(request, 'dashboard/article_list.html', context)

def article_detail(request, slug):
    """View for displaying a single article"""
    article = get_object_or_404(Article, slug=slug)
    
    # Get related articles based on tags
    article_tags = article.get_tags_list()
    related_articles = []
    
    if article_tags:
        # Filter articles that share tags with this article
        for tag in article_tags:
            related = Article.objects.filter(tags__icontains=tag).exclude(id=article.id)
            for r in related:
                if r not in related_articles:
                    related_articles.append(r)
                    if len(related_articles) >= 3:
                        break
            if len(related_articles) >= 3:
                break
    
    context = {
        'article': article,
        'related_articles': related_articles[:3],
    }
    
    return render(request, 'dashboard/article_detail.html', context)

def project_list(request):
    """View for listing projects with filtering"""
    # Get query parameters
    q = request.GET.get('q', '')
    tech = request.GET.get('tech', '')
    
    # Base queryset
    projects = Project.objects.all()
    
    # Apply search filter
    if q:
        projects = projects.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q) |
            Q(technologies__icontains=q)
        )
    
    # Apply technology filter
    if tech:
        projects = projects.filter(technologies__icontains=tech)
    
    # Get unique technologies for filter sidebar
    all_technologies = set()
    for project in Project.objects.all():
        for tech in project.get_technologies_list():
            all_technologies.add(tech)
    
    context = {
        'projects': projects,
        'query': q,
        'tech_filter': tech,
        'all_technologies': sorted(all_technologies),
    }
    
    return render(request, 'dashboard/project_list.html', context)

def project_detail(request, slug):
    """View for displaying a single project and handling feedback"""
    project = get_object_or_404(Project, slug=slug)
    feedback = project.feedback.all()
    
    # Increment view counter
    project.views += 1
    project.save()
    
    # Handle feedback form submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ProjectFeedbackForm(request.POST)
        if form.is_valid():
            # Check if user already provided feedback
            existing_feedback = ProjectFeedback.objects.filter(
                project=project, 
                user=request.user
            ).first()
            
            if existing_feedback:
                # Update existing feedback
                existing_feedback.comment = form.cleaned_data['comment']
                existing_feedback.rating = form.cleaned_data['rating']
                existing_feedback.save()
                messages.success(request, "Your feedback has been updated!")
            else:
                # Create new feedback
                new_feedback = form.save(commit=False)
                new_feedback.project = project
                new_feedback.user = request.user
                new_feedback.save()
                
                # Update project's comments count
                project.comments_count += 1
                project.save()
                
                messages.success(request, "Your feedback has been submitted!")
            
            return redirect('dashboard:project_detail', slug=slug)
    else:
        form = ProjectFeedbackForm()
    
    # Get similar projects based on technologies
    project_techs = project.get_technologies_list()
    similar_projects = []
    
    if project_techs:
        # Filter projects that share technologies with this project
        for tech in project_techs:
            similar = Project.objects.filter(technologies__icontains=tech).exclude(id=project.id)
            for s in similar:
                if s not in similar_projects:
                    similar_projects.append(s)
                    if len(similar_projects) >= 3:
                        break
            if len(similar_projects) >= 3:
                break
    
    context = {
        'project': project,
        'feedback': feedback,
        'form': form,
        'similar_projects': similar_projects[:3],
    }
    
    return render(request, 'dashboard/project_detail.html', context)

def resource_list(request):
    """View for listing resources with filtering by category"""
    # Get query parameters
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    
    # Base queryset
    resources = Resource.objects.all()
    
    # Apply search filter
    if q:
        resources = resources.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q) |
            Q(tags__icontains=q)
        )
    
    # Apply category filter
    if category:
        resources = resources.filter(category=category)
    
    # Apply tag filter
    if tag:
        resources = resources.filter(tags__icontains=tag)
    
    # Get unique tags for filter sidebar
    all_tags = set()
    for resource in Resource.objects.all():
        for tag in resource.get_tags_list():
            all_tags.add(tag)
    
    context = {
        'resources': resources,
        'query': q,
        'category_filter': category,
        'tag_filter': tag,
        'all_tags': sorted(all_tags),
        'categories': Resource.CATEGORY_CHOICES,
    }
    
    return render(request, 'dashboard/resource_list.html', context)

def resource_detail(request, slug):
    """View for displaying a single resource"""
    resource = get_object_or_404(Resource, slug=slug)
    
    # Get related resources based on tags and category
    related_resources = Resource.objects.filter(
        Q(category=resource.category) | 
        Q(tags__icontains=resource.tags)
    ).exclude(id=resource.id)[:3]
    
    context = {
        'resource': resource,
        'related_resources': related_resources,
    }
    
    return render(request, 'dashboard/resource_detail.html', context)

def community(request):
    """View for displaying community wins and challenge solutions"""
    from wins.models import DailyWin
    from challenges.models import ChallengeSolution
    
    # Get public wins
    wins = DailyWin.objects.filter(is_public=True).order_by('-created_at')
    
    # Get challenge solutions
    challenge_solutions = ChallengeSolution.objects.filter(is_correct=True).order_by('-submitted_at')
    
    return render(request, 'dashboard/community.html', {
        'wins': wins, 
        'challenge_solutions': challenge_solutions
    })

def tech_news(request):
    """View for displaying technology news articles"""
    # Get query parameters
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 12))
    
    # Initialize news service
    news_service = get_news_service()
    
    # Fetch articles based on search query
    if query:
        news_data = news_service.search_tech_news(query, page=page, page_size=page_size)
    else:
        news_data = news_service.get_tech_news(page=page, page_size=page_size)
    
    # Process response
    articles = news_data.get('articles', [])
    total_results = news_data.get('totalResults', 0)
    status = news_data.get('status', 'error')
    error_message = news_data.get('message', None) if status == 'error' else None
    
    # Calculate pagination information
    total_pages = (total_results + page_size - 1) // page_size if total_results > 0 else 1
    has_next = page < total_pages
    has_prev = page > 1
    
    # Add featured articles from our database
    featured_articles = Article.objects.filter(is_featured=True, tags__icontains='technology')[:3]
    
    context = {
        'articles': articles,
        'featured_articles': featured_articles,
        'total_results': total_results,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'has_next': has_next,
        'has_prev': has_prev,
        'query': query,
        'error_message': error_message,
    }
    
    return render(request, 'dashboard/tech_news.html', context)