status_code, 302)
        self.assertTrue(Challenge.objects.filter(title='Test Challenge').exists())
```

## Code Architecture Guidelines

### 1. Django App Structure

#### App Organization
Each Django app should follow this structure:
```
app_name/
├── migrations/          # Database migrations
├── templates/           # App-specific templates
│   └── app_name/       # Namespaced templates
├── static/             # App-specific static files
│   └── app_name/       # Namespaced static files
├── admin.py            # Admin interface configuration
├── apps.py             # App configuration
├── forms.py            # Django forms
├── models.py           # Database models
├── urls.py             # URL patterns
├── views.py            # View functions/classes
└── tests.py            # Unit tests
```

#### Model Guidelines
```python
# Good model example
class Challenge(models.Model):
    """
    Represents a coding challenge that users can solve.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('hard', 'Hard')
    ]
    
    title = models.CharField(max_length=200, help_text="Challenge title")
    description = models.TextField(help_text="Detailed challenge description")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
    
    def __str__(self):
        return self.title
    
    def get_difficulty_color(self):
        """Returns CSS color class based on difficulty."""
        color_map = {
            'beginner': 'green-600',
            'intermediate': 'yellow-600',
            'hard': 'red-600'
        }
        return color_map.get(self.difficulty, 'blue-600')
```

#### View Guidelines
```python
# Function-based view example
@login_required
def challenge_detail(request, pk):
    """
    Display a single challenge with user's solution status.
    """
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    
    # Get user's previous solution
    user_solution = ChallengeSolution.objects.filter(
        challenge=challenge,
        user=request.user
    ).order_by('-submitted_at').first()
    
    context = {
        'challenge': challenge,
        'user_solution': user_solution,
        'form': ChallengeSolutionForm(),
    }
    
    return render(request, 'challenges/challenge_detail.html', context)
```

### 2. Frontend Development

#### Template Structure
```html
<!-- Base template structure -->
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Boost.dev{% endblock %}</title>
    <link href="{% static 'css/dist/styles.css' %}" rel="stylesheet">
</head>
<body class="bg-gray-900 text-white">
    {% include 'components/navbar.html' %}
    
    <main class="container mx-auto px-4 py-8">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} mb-4">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}
        {% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

#### Tailwind CSS Usage
```css
/* Use utility classes for consistent styling */
.btn-primary {
    @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded transition duration-200;
}

.card {
    @apply bg-gray-800 rounded-lg shadow-lg p-6;
}

.form-input {
    @apply w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500;
}
```

### 3. Service Layer Pattern

#### External API Services
```python
# services/ai_challenge.py
import os
import google.generativeai as genai
from django.conf import settings

class GeminiAIService:
    """Service for interacting with Google Gemini AI API."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_names = [
            "models/gemini-1.5-pro",
            "models/gemini-1.5-flash",
            "models/gemini-2.0-flash-lite",
        ]
    
    def get_challenge_feedback(self, solution_text, challenge, username):
        """
        Generate AI feedback for a challenge solution.
        
        Args:
            solution_text (str): User's solution
            challenge (Challenge): Challenge instance
            username (str): User's name for personalization
            
        Returns:
            str: AI-generated feedback
        """
        prompt = self._build_feedback_prompt(solution_text, challenge, username)
        return self._call_ai_with_fallback(prompt)
    
    def _call_ai_with_fallback(self, prompt):
        """Try multiple models with fallback."""
        for model_name in self.model_names:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Model {model_name} failed: {e}")
                continue
        
        # Fallback response if all models fail
        return "Our AI assistant is taking a break, but your solution shows real effort!"
```

## Database Design Patterns

### 1. Model Relationships

#### One-to-One Relationships
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
```

#### Foreign Key Relationships
```python
class Challenge(models.Model):
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_challenges'
    )

class ChallengeSolution(models.Model):
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE, 
        related_name='solutions'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='challenge_solutions'
    )
```

#### Many-to-Many Relationships
```python
class DailyWin(models.Model):
    celebrations = models.ManyToManyField(
        User, 
        related_name='celebrated_wins', 
        blank=True
    )
```

### 2. Query Optimization

#### Efficient Queries
```python
# Good: Use select_related for foreign keys
challenges = Challenge.objects.select_related('created_by').all()

# Good: Use prefetch_related for many-to-many
wins = DailyWin.objects.prefetch_related('celebrations').all()

# Good: Filter early and limit results
recent_challenges = Challenge.objects.filter(
    is_approved=True,
    created_at__gte=timezone.now() - timedelta(days=30)
).order_by('-created_at')[:10]
```

#### Avoid N+1 Queries
```python
# Bad: N+1 query problem
for challenge in challenges:
    print(challenge.created_by.username)  # Each iteration hits DB

# Good: Use select_related
challenges = Challenge.objects.select_related('created_by').all()
for challenge in challenges:
    print(challenge.created_by.username)  # No additional DB hits
```

## Error Handling and Logging

### 1. Exception Handling

#### View Error Handling
```python
@login_required
def submit_solution(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    
    if request.method == 'POST':
        form = ChallengeSolutionForm(request.POST)
        if form.is_valid():
            try:
                solution = form.save(commit=False)
                solution.challenge = challenge
                solution.user = request.user
                
                # Get AI feedback with error handling
                try:
                    solution.ai_feedback = get_challenge_feedback(
                        solution.solution_text, 
                        challenge, 
                        request.user.username
                    )
                except Exception as e:
                    logger.error(f"AI feedback error: {e}")
                    solution.ai_feedback = "Feedback temporarily unavailable."
                
                solution.save()
                messages.success(request, "Solution submitted successfully!")
                
            except Exception as e:
                logger.error(f"Solution submission error: {e}")
                messages.error(request, "Error submitting solution. Please try again.")
        
        else:
            messages.error(request, "Please correct the form errors.")
    
    return redirect('challenge_detail', pk=pk)
```

#### Service Error Handling
```python
def get_challenge_feedback(solution_text, challenge, username):
    """Get AI feedback with comprehensive error handling."""
    try:
        service = GeminiAIService()
        return service.get_challenge_feedback(solution_text, challenge, username)
    except APIError as e:
        logger.error(f"AI API error: {e}")
        return f"Great effort on your solution, {username}! Keep practicing."
    except Exception as e:
        logger.error(f"Unexpected error in AI feedback: {e}")
        return "Your solution shows good thinking. Keep it up!"
```

### 2. Logging Configuration

#### Settings Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'challenges': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Performance Optimization

### 1. Database Optimization

#### Indexing Strategy
```python
class Challenge(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['difficulty', 'created_at']),
            models.Index(fields=['is_approved', 'difficulty']),
        ]
```

#### Query Optimization
```python
# Use pagination for large datasets
from django.core.paginator import Paginator

def challenge_list(request):
    challenges = Challenge.objects.filter(is_approved=True).select_related('created_by')
    paginator = Paginator(challenges, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'challenges/list.html', {'page_obj': page_obj})
```

### 2. Caching Strategy

#### View-Level Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def tech_news(request):
    """Cached tech news view."""
    news_data = get_cached_news()
    return render(request, 'dashboard/tech_news.html', {'news': news_data})
```

#### Template Fragment Caching
```html
{% load cache %}
{% cache 500 challenge_list request.user.username %}
    <!-- Expensive template rendering -->
    {% for challenge in challenges %}
        {% include 'challenges/challenge_card.html' %}
    {% endfor %}
{% endcache %}
```

## Security Best Practices

### 1. Input Validation

#### Form Validation
```python
from django import forms
from django.core.exceptions import ValidationError

class ChallengeSolutionForm(forms.ModelForm):
    class Meta:
        model = ChallengeSolution
        fields = ['solution_text']
        widgets = {
            'solution_text': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Enter your solution here...',
                'class': 'form-input'
            })
        }
    
    def clean_solution_text(self):
        solution = self.cleaned_data['solution_text']
        if len(solution.strip()) < 10:
            raise ValidationError("Solution must be at least 10 characters long.")
        return solution
```

#### User Input Sanitization
```python
from django.utils.html import escape
from django.template.defaultfilters import linebreaks

def render_user_content(content):
    """Safely render user-generated content."""
    escaped_content = escape(content)
    return linebreaks(escaped_content)
```

### 2. Authentication and Authorization

#### Permission Decorators
```python
from django.contrib.auth.decorators import login_required, user_passes_test

def is_challenge_creator(user):
    return user.is_authenticated and user.created_challenges.exists()

@login_required
@user_passes_test(is_challenge_creator)
def advanced_challenge_view(request):
    """View only for users who have created challenges."""
    pass
```

#### Model-Level Permissions
```python
class ChallengeSolution(models.Model):
    # ... fields ...
    
    def can_edit(self, user):
        """Check if user can edit this solution."""
        return self.user == user
    
    def can_view(self, user):
        """Check if user can view this solution."""
        return self.user == user or user.is_staff
```

## Deployment Guidelines

### 1. Production Settings

#### Environment-Specific Settings
```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'boost-dev.com']

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Heroku Deployment

#### Procfile Configuration
```
web: gunicorn boost_dev.wsgi:application
release: python manage.py migrate
```

#### Runtime Configuration
```
# runtime.txt
python-3.11.0
```

#### Environment Variables
```bash
# Required Heroku Config Vars
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DATABASE_URL=postgres://...
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set NEWS_API_KEY=your_news_key
heroku config:set DEBUG=False
```

## Troubleshooting Guide

### 1. Common Issues

#### Migration Problems
```bash
# Reset migrations (development only)
python manage.py migrate app_name zero
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate

# Fix migration conflicts
python manage.py migrate --fake app_name migration_number
```

#### Tailwind CSS Issues
```bash
# Rebuild Tailwind CSS
python manage.py tailwind build

# Clear cache and rebuild
rm -rf theme/static_src/node_modules
python manage.py tailwind install
python manage.py tailwind build
```

#### Static Files Problems
```bash
# Collect static files
python manage.py collectstatic --clear

# Check static files configuration
python manage.py findstatic filename.css
```

### 2. Debugging Tips

#### Debug Toolbar (Development)
```python
# Add to INSTALLED_APPS in development
INSTALLED_APPS += ['debug_toolbar']

# Add middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Configure internal IPs
INTERNAL_IPS = ['127.0.0.1']
```

#### Database Query Debugging
```python
from django.db import connection

# Print all queries
print(connection.queries)

# Count queries
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test_view():
    # Your test code
    print(f"Number of queries: {len(connection.queries)}")
```

## Contributing Guidelines

### 1. Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No hardcoded secrets or sensitive data
- [ ] Database migrations are reviewed
- [ ] Performance impact is considered

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)

## Additional Notes
```

This development guide provides comprehensive guidelines for maintaining and extending the Boost.dev application. Follow these patterns and practices to ensure code quality, security, and maintainability.
