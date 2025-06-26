# API Reference Documentation

## Overview
This document provides comprehensive API reference for Boost.dev's internal endpoints and external service integrations.

## Internal API Endpoints

### Authentication Endpoints

#### Login
- **URL**: `/login/`
- **Method**: `GET`, `POST`
- **Description**: User authentication
- **Parameters**:
  - `username`: User's username or email
  - `password`: User's password
- **Response**: Redirect to dashboard on success

#### Registration  
- **URL**: `/register/`
- **Method**: `GET`, `POST`
- **Description**: New user registration
- **Parameters**:
  - `username`: Unique username
  - `email`: User email
  - `password1`: Password
  - `password2`: Password confirmation
- **Response**: Redirect to dashboard with new user profile

#### Social Authentication
- **URLs**: `/accounts/github/login/`, `/accounts/google-oauth2/login/`, etc.
- **Method**: `GET`
- **Description**: OAuth2 social authentication
- **Response**: Redirect to dashboard after successful authentication

### Challenge Endpoints

#### List Challenges
- **URL**: `/challenges/`
- **Method**: `GET`
- **Description**: List all approved challenges with filtering and pagination
- **Query Parameters**:
  - `difficulty`: Filter by difficulty (`beginner`, `intermediate`, `hard`)
  - `q`: Search query for title/description
  - `page`: Page number for pagination (default: 1)
- **Response**: Paginated challenge list

#### Challenge Detail
- **URL**: `/challenges/<int:pk>/`
- **Method**: `GET`
- **Description**: Display single challenge with user solution status
- **Response**: Challenge details, hints, user's previous solution

#### Submit Solution
- **URL**: `/challenges/<int:pk>/submit/`
- **Method**: `POST`
- **Description**: Submit solution to challenge
- **Parameters**:
  - `solution_text`: User's code solution
- **Response**: AI feedback and solution storage
- **Points Awarded**: 
  - Beginner: +30 points
  - Intermediate: +45 points
  - Hard: +60 points

#### Create Challenge
- **URL**: `/challenges/new/`
- **Method**: `GET`, `POST`
- **Description**: Create new challenge
- **Parameters**:
  - `title`: Challenge title
  - `description`: Challenge description
  - `difficulty`: Difficulty level
  - `hints`: JSON array of hints
- **Points Awarded**: +40 points

#### Generate AI Challenge
- **URL**: `/challenges/generate/`
- **Method**: `POST`
- **Description**: Generate new challenge using AI
- **Parameters**:
  - `difficulty`: Target difficulty level
  - `topic`: Challenge topic/theme
- **Response**: AI-generated challenge with structured format

### User Endpoints

#### User Profile
- **URL**: `/users/profile/`
- **Method**: `GET`, `POST`
- **Description**: View and update user profile
- **Parameters** (POST):
  - `bio`: User biography
  - `github_username`: GitHub username
  - `experience_level`: Experience level
- **Points Awarded**: +15 points (on update)

#### User Progress
- **URL**: `/users/progress/` (context processor)
- **Method**: Context data
- **Description**: User's current progress, level, and achievements
- **Response**: Progress percentage, level info, recent achievements

### Wins Endpoints

#### Submit Win
- **URL**: `/wins/submit/`
- **Method**: `GET`, `POST`
- **Description**: Submit daily win
- **Parameters**:
  - `content`: Win description
  - `is_public`: Whether win is publicly visible
- **Points Awarded**: +20 points

#### My Wins
- **URL**: `/wins/my-wins/`
- **Method**: `GET`
- **Description**: List user's personal wins
- **Response**: Paginated wins list with edit options

#### Community Wins
- **URL**: `/wins/community/`
- **Method**: `GET`
- **Description**: List public community wins
- **Response**: Public wins with celebration counts

#### Toggle Celebration
- **URL**: `/wins/celebrate/<int:win_id>/`
- **Method**: `POST`
- **Description**: Celebrate/uncelebrate a win
- **Response**: Updated celebration status

### Dashboard Endpoints

#### Main Dashboard
- **URL**: `/dashboard/`
- **Method**: `GET`
- **Description**: User dashboard with recent activity
- **Response**: Recent challenges, wins, progress summary

#### Community Hub
- **URL**: `/dashboard/community/`
- **Method**: `GET`
- **Description**: Community interaction hub
- **Response**: Community posts, discussions

#### Tech News
- **URL**: `/dashboard/tech_news/`
- **Method**: `GET`
- **Description**: Curated technology news
- **Response**: Categorized news articles with caching

## External API Integrations

### Google Gemini AI API

#### Challenge Feedback
```python
def get_challenge_feedback(solution_text, challenge, username):
    """
    Get AI feedback on challenge solution
    
    Args:
        solution_text (str): User's solution code
        challenge (obj): Challenge object with context
        username (str): User's name for personalization
    
    Returns:
        str: Personalized AI feedback (3-4 sentences)
    """
```

**Model Fallback Order**:
1. `gemini-1.5-pro`
2. `gemini-1.5-flash` 
3. `gemini-2.0-flash-lite`
4. `gemini-1.5-flash-8b`

**Response Format**: Encouraging feedback focusing on:
- Specific strengths acknowledgment
- Gentle improvement guidance
- Growth mindset reinforcement
- Hints or next challenges

#### Challenge Generation
```python
def generate_new_challenge(difficulty, topic, username):
    """
    Generate new challenge using AI
    
    Args:
        difficulty (str): Target difficulty level
        topic (str): Challenge topic/domain
        username (str): User for personalization
    
    Returns:
        str: Structured challenge text with:
            - TITLE: Challenge title
            - DESCRIPTION: Detailed description
            - HINT 1: First hint
            - HINT 2: Second hint  
            - HINT 3: Third hint
    """
```

### News API Integration

#### Tech News Fetching
```python
def get_tech_news(category, query_params):
    """
    Fetch categorized technology news
    
    Categories:
        - Latest Tech News
        - Developer News
        - Software Updates
        - Cybersecurity & Hacking
        - Imposter Syndrome Tips
    
    Features:
        - 30-minute server-side caching
        - Rate limiting protection
        - Error handling with graceful degradation
    """
```

## Data Models API

### User Progress Model
```python
class UserProgress:
    def calculate_percentage():
        """Calculate progress to next level"""
        
    def update_level():
        """Update level based on points, return if leveled up"""
        
    def add_points(points):
        """Add points and auto-level if threshold reached"""
        
    def get_level_color():
        """Get UI color class for current level"""
```

### Challenge Model
```python
class Challenge:
    def get_difficulty_color():
        """Get Tailwind color class for difficulty"""
        # Returns: green-600, yellow-600, red-600
```

### Daily Win Model
```python
class DailyWin:
    def is_today():
        """Check if win was created today"""
        
    def celebration_count():
        """Get total celebration count"""
        
    def is_celebrated_by(user):
        """Check if user has celebrated this win"""
        
    def toggle_celebration(user):
        """Toggle user's celebration status"""
```

## Authentication Flow

### Standard Authentication
1. `POST /login/` with credentials
2. Django session creation
3. Redirect to `/dashboard/`
4. Access protected endpoints with session

### Social Authentication (OAuth2)
1. `GET /accounts/{provider}/login/`
2. OAuth2 redirect to provider
3. Provider authorization
4. Callback with authorization code
5. Token exchange and user creation/login
6. Redirect to `/dashboard/`

## Error Handling

### API Error Responses

#### Authentication Errors
- **401 Unauthorized**: Invalid credentials
- **403 Forbidden**: Insufficient permissions
- **Redirect**: Login required for protected endpoints

#### Validation Errors
- **400 Bad Request**: Form validation failures
- **404 Not Found**: Resource does not exist
- **422 Unprocessable Entity**: Business logic violations

#### External Service Errors
- **503 Service Unavailable**: External API failures
- **Graceful Degradation**: Fallback responses for AI services

### Error Response Format
```json
{
    "error": "Error message",
    "field_errors": {
        "field_name": ["Field-specific error messages"]
    },
    "status": "error"
}
```

## Rate Limiting

### External APIs
- **Gemini API**: Managed via multiple model fallback
- **News API**: 30-minute caching to reduce calls
- **Social Auth**: Provider-specific limits

### Internal Endpoints
- Session-based rate limiting via Django
- Database connection pooling
- Query optimization for performance

## Response Formats

### Success Responses
```python
# Redirect responses (most endpoints)
HttpResponseRedirect('/target/url/')

# Template responses
render(request, 'template.html', context)

# JSON responses (future API endpoints)
JsonResponse({'status': 'success', 'data': data})
```

### Context Data Format
```python
{
    'user_progress': UserProgress object,
    'recent_achievements': QuerySet,
    'level_progress': Integer (0-100),
    'user_solutions': Dict mapping challenge_id to solution,
    'notifications': QuerySet,
}
```

## Security Considerations

### CSRF Protection
- All POST endpoints require CSRF tokens
- Django middleware handles validation
- Social auth endpoints protected

### User Data Protection
- User solutions stored securely
- AI feedback anonymized in requests
- Social auth tokens handled by django-social-auth

### API Key Management
- Environment variable storage
- No hardcoded credentials
- Separate development/production keys

## Performance Optimization

### Database Queries
- Pagination for large lists (6 items per page)
- Query prefetching for related objects
- Indexed fields for search operations

### Caching Strategy
- News API responses cached 30 minutes
- Static files cached with WhiteNoise
- Template fragment caching (future)

### External Service Optimization
- AI model fallback for reliability
- Async processing for non-critical operations
- Error handling with user-friendly fallbacks
