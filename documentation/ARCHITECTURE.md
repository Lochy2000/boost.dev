# Boost.dev Architecture Documentation

## Overview
Boost.dev is a Django-based web application designed to help developers overcome imposter syndrome through interactive challenges, community support, and AI-powered feedback.

## Technology Stack

### Backend
- **Framework**: Django 5.2
- **Database**: PostgreSQL (via dj_database_url)
- **Authentication**: Django Auth + Social Auth (GitHub, Google, Facebook, LinkedIn)
- **Environment Management**: python-dotenv
- **Static Files**: WhiteNoise with compressed manifest storage

### Frontend
- **CSS Framework**: Tailwind CSS (via django-tailwind)
- **Admin Interface**: Grappelli
- **Responsive Design**: Mobile-first approach

### External Services
- **AI Integration**: Google Gemini API for challenge feedback and generation
- **News API**: Tech news aggregation
- **Social Authentication**: OAuth2 providers

## Project Structure

```
boost.dev/
├── boost_dev/           # Main Django project
│   ├── settings.py      # Configuration
│   ├── urls.py          # Root URL patterns
│   └── wsgi.py         # WSGI configuration
├── challenges/          # Coding challenges system
├── dashboard/           # Main dashboard and community features
├── users/              # User management and progress tracking
├── wins/               # Daily wins system
├── services/           # External API integrations
├── theme/              # Tailwind CSS theme
├── static/             # Static files
├── documentation/      # Project documentation
└── requirements.txt    # Python dependencies
```

## Application Architecture

### Core Applications

#### 1. Users App (`users/`)
**Purpose**: User management, authentication, progress tracking, and achievements

**Key Models**:
- `UserProfile`: Extended user information
- `UserProgress`: Points, levels, achievements
- `Achievement`: Available achievements
- `UserAchievement`: User-earned achievements
- `UserFlag`: Temporary event notifications
- `Notification`: User notifications

**Key Features**:
- Social authentication integration
- Progress tracking with 5-level system
- Achievement system
- User profile management

#### 2. Challenges App (`challenges/`)
**Purpose**: Coding challenges with AI feedback

**Key Models**:
- `Challenge`: Coding challenges with difficulty levels
- `ChallengeSolution`: User submissions with AI feedback
- `QuoteSubmission`: Motivational quotes (temporary)

**Key Features**:
- Challenge creation and management
- AI-powered solution feedback
- Difficulty-based filtering
- Progress tracking integration

#### 3. Dashboard App (`dashboard/`)
**Purpose**: Main user interface and community features

**Key Features**:
- User dashboard
- Community hub
- Tech news integration
- Landing page

#### 4. Wins App (`wins/`)
**Purpose**: Daily wins tracking and community celebration

**Key Models**:
- `DailyWin`: User daily achievements
- Win celebrations and sharing

**Key Features**:
- Daily win submission
- Community win sharing
- Celebration system

#### 5. Services App (`services/`)
**Purpose**: External API integrations and AI services

**Key Modules**:
- `ai_challenge.py`: Gemini AI integration
- `ai_feedback.py`: AI feedback generation
- `news/`: News API integration
- `weather.py`: Weather data (if used)

## URL Architecture

### Root URL Configuration (`boost_dev/urls.py`)
```python
urlpatterns = [
    path('', dashboard_views.home, name='home'),                    # Landing page
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('register/', user_views.register_view, name='register'),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('login/', user_views.login_view, name='login'),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('challenges/', include('challenges.urls')),
    path('wins/', include('wins.urls')),
]
```

### App-Specific URL Patterns

#### Dashboard URLs (`dashboard/urls.py`)
- `/dashboard/` - Main dashboard
- `/dashboard/community/` - Community hub
- `/dashboard/tech_news/` - Tech news feed

#### Challenges URLs (`challenges/urls.py`)
- `/challenges/` - Challenge list
- `/challenges/new/` - Create challenge
- `/challenges/<id>/` - Challenge detail
- `/challenges/<id>/submit/` - Submit solution
- `/challenges/generate/` - AI challenge generation

#### Wins URLs (`wins/urls.py`)
- `/wins/submit/` - Submit daily win
- `/wins/my-wins/` - User's wins history
- `/wins/community/` - Community wins
- `/wins/celebrate/<id>/` - Celebrate win

## Database Schema

### User Progress System
```
UserProgress:
- points: IntegerField (cumulative points)
- level: IntegerField (1-5)
- next_level_threshold: IntegerField

Level Thresholds:
- Level 1 (Rookie): 0-29 points
- Level 2 (Explorer): 30-69 points  
- Level 3 (Hacker): 70-119 points
- Level 4 (Wizard): 120-199 points
- Level 5 (Master): 200+ points
```

### Points System
- Daily win: +20 points
- Beginner challenge: +30 points
- Intermediate challenge: +45 points
- Hard challenge: +60 points
- Creating challenge: +40 points
- Profile update: +15 points

## API Integration Patterns

### AI Services (Gemini API)
```python
# Challenge feedback generation
feedback = get_challenge_feedback(solution_text, challenge, username)

# New challenge generation  
challenge = generate_new_challenge(difficulty, topic, username)
```

### News API Integration
- Cached tech news fetching
- Category-based filtering
- Rate limiting consideration

## Authentication Flow

### Standard Authentication
1. User registration/login via Django forms
2. Profile creation signal triggers
3. Initial UserProgress and achievements created

### Social Authentication
1. OAuth2 flow with external providers
2. User profile auto-creation
3. Seamless integration with existing accounts

## Development Patterns

### Model Signals
- Automatic profile creation on user registration
- Achievement awarding on level-up
- Progress tracking automation

### Form Handling
- Django forms for user input
- CSRF protection
- Field validation

### Template Organization
- App-specific template directories
- Shared base templates
- Component-based design

## Security Considerations

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection
- `GEMINI_API_KEY`: AI service authentication
- `NEWS_API_KEY`: News service authentication
- Social auth credentials

### Security Measures
- CSRF protection
- User authentication requirements
- Environment-based configuration
- Secure static file serving

## Deployment Architecture

### Heroku Configuration
- `Procfile`: Web server configuration
- Environment variables via Config Vars
- Static file serving via WhiteNoise
- PostgreSQL database addon

### Static Files
- Collected to `staticfiles/` directory
- Served via WhiteNoise in production
- Tailwind CSS compilation

## Performance Considerations

### Database Optimization
- Query optimization for challenge lists
- Pagination for large datasets
- Related object prefetching

### Caching Strategy
- News API response caching
- Static file compression
- Template fragment caching (future enhancement)

## Future Scalability

### Planned Enhancements
- REST API for mobile app
- Real-time notifications
- Advanced analytics
- Extended AI integration

### Architecture Flexibility
- Modular app design
- Service-oriented external integrations
- Database abstraction layer
