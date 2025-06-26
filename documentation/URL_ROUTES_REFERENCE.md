wins/my-wins/` | `views.my_wins` | `wins:my_wins` | User's wins history |
| `/wins/community/` | `views.community_wins` | `wins:community_wins` | Community wins feed |
| `/wins/toggle-public/<int:win_id>/` | `views.toggle_public` | `wins:toggle_public` | Toggle win visibility |
| `/wins/celebrate/<int:win_id>/` | `views.toggle_celebration` | `wins:toggle_celebration` | Celebrate/uncelebrate win |

### Example URLs
- `https://boost-dev.herokuapp.com/wins/submit/`
- `https://boost-dev.herokuapp.com/wins/my-wins/`
- `https://boost-dev.herokuapp.com/wins/community/`
- `https://boost-dev.herokuapp.com/wins/celebrate/42/`

## Authentication URLs

### Django Social Auth Routes (`social_django.urls`)
| URL Pattern | Provider | Description |
|-------------|----------|-------------|
| `/accounts/login/github/` | GitHub | GitHub OAuth login |
| `/accounts/login/google-oauth2/` | Google | Google OAuth login |
| `/accounts/login/facebook/` | Facebook | Facebook OAuth login |
| `/accounts/login/linkedin-oauth2/` | LinkedIn | LinkedIn OAuth login |
| `/accounts/complete/github/` | GitHub | GitHub OAuth callback |
| `/accounts/complete/google-oauth2/` | Google | Google OAuth callback |
| `/accounts/complete/facebook/` | Facebook | Facebook OAuth callback |
| `/accounts/complete/linkedin-oauth2/` | LinkedIn | LinkedIn OAuth callback |

### Standard Authentication
| URL Pattern | View Function | URL Name | Description |
|-------------|---------------|----------|-------------|
| `/login/` | `user_views.login_view` | `login` | Standard login form |
| `/register/` | `user_views.register_view` | `register` | User registration form |
| `/logout/` | `user_views.logout_view` | `logout` | User logout |

### Example URLs
- `https://boost-dev.herokuapp.com/login/`
- `https://boost-dev.herokuapp.com/register/`
- `https://boost-dev.herokuapp.com/accounts/login/github/`

## Admin Interface URLs

### Django Admin
| URL Pattern | Description |
|-------------|-------------|
| `/admin/` | Django admin interface |
| `/grappelli/` | Enhanced admin interface (Grappelli) |

### Admin Model URLs
- `/admin/auth/user/` - User management
- `/admin/challenges/challenge/` - Challenge management
- `/admin/challenges/challengesolution/` - Solution management
- `/admin/users/userprofile/` - User profile management
- `/admin/users/userprogress/` - User progress management
- `/admin/users/achievement/` - Achievement management
- `/admin/wins/dailywin/` - Daily wins management

## API Endpoint Patterns

### RESTful URL Design
The application follows RESTful URL patterns:

#### Collection URLs (List/Create)
- `GET /challenges/` - List challenges
- `POST /challenges/new/` - Create challenge
- `GET /wins/my-wins/` - List user's wins
- `POST /wins/submit/` - Create new win

#### Resource URLs (Read/Update/Delete)
- `GET /challenges/{id}/` - View specific challenge
- `POST /challenges/{id}/submit/` - Submit solution to challenge
- `GET /wins/view/{id}/` - View specific win
- `POST /wins/celebrate/{id}/` - Toggle celebration on win

#### Action URLs (Special Operations)
- `POST /challenges/generate/` - Generate AI challenge
- `POST /wins/toggle-public/{id}/` - Toggle win visibility

## HTTP Methods and Actions

### Challenge Endpoints
```http
GET    /challenges/                 # List challenges with filters
GET    /challenges/new/             # Show create form
POST   /challenges/new/             # Create new challenge
GET    /challenges/{id}/            # Show challenge detail
POST   /challenges/{id}/submit/     # Submit solution
POST   /challenges/generate/        # Generate AI challenge
```

### Wins Endpoints
```http
GET    /wins/submit/                # Show win submission form
POST   /wins/submit/                # Submit new win
GET    /wins/my-wins/               # List user's wins
GET    /wins/community/             # List public wins
POST   /wins/celebrate/{id}/        # Toggle celebration
POST   /wins/toggle-public/{id}/    # Toggle visibility
```

### Dashboard Endpoints
```http
GET    /dashboard/                  # Main dashboard
GET    /dashboard/community/        # Community hub
GET    /dashboard/tech_news/        # Tech news feed
```

## URL Parameters and Query Strings

### Challenge List Parameters
```
GET /challenges/?difficulty=beginner&q=python&page=2

Parameters:
- difficulty: Filter by difficulty level
  - Values: beginner, intermediate, hard
- q: Search query for title/description
- page: Pagination page number (default: 1)
```

### Challenge Detail Parameters
```
GET /challenges/15/
POST /challenges/15/submit/

URL Parameters:
- pk (int): Challenge primary key/ID
```

### Wins Parameters
```
POST /wins/celebrate/42/
POST /wins/toggle-public/42/

URL Parameters:
- win_id (int): Daily win primary key/ID
```

## URL Name Patterns and Reverse Lookups

### Using URL Names in Templates
```html
<!-- Dashboard links -->
<a href="{% url 'dashboard:dashboard' %}">Dashboard</a>
<a href="{% url 'dashboard:community' %}">Community</a>
<a href="{% url 'dashboard:tech_news' %}">Tech News</a>

<!-- Challenge links -->
<a href="{% url 'challenges' %}">All Challenges</a>
<a href="{% url 'new_challenge' %}">Create Challenge</a>
<a href="{% url 'challenge_detail' pk=challenge.id %}">View Challenge</a>

<!-- Wins links -->
<a href="{% url 'wins:submit_win' %}">Submit Win</a>
<a href="{% url 'wins:my_wins' %}">My Wins</a>
<a href="{% url 'wins:community_wins' %}">Community Wins</a>

<!-- Authentication links -->
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'register' %}">Register</a>
```

### Using URL Names in Views
```python
from django.shortcuts import redirect
from django.urls import reverse

# Redirect examples
return redirect('dashboard:dashboard')
return redirect('challenge_detail', pk=challenge.id)
return redirect('wins:my_wins')

# URL generation examples
challenge_url = reverse('challenge_detail', kwargs={'pk': 15})
submit_url = reverse('submit_solution', kwargs={'pk': 15})
```

## Response Formats and Content Types

### HTML Responses (Default)
```http
GET /challenges/
Content-Type: text/html

Returns: Rendered HTML template with challenge list
```

### Form Submissions
```http
POST /challenges/new/
Content-Type: application/x-www-form-urlencoded

Data: title=Challenge+Title&description=Description&difficulty=beginner
Response: Redirect to challenge detail or form with errors
```

### AJAX Requests (Future Enhancement)
```http
POST /wins/celebrate/42/
Content-Type: application/json
Accept: application/json

Response: {"status": "success", "celebrated": true, "count": 5}
```

## Error Handling and Status Codes

### Success Responses
- `200 OK` - Successful GET requests
- `302 Found` - Successful POST with redirect
- `201 Created` - Resource created (future API)

### Client Error Responses
- `400 Bad Request` - Form validation errors
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource doesn't exist

### Server Error Responses
- `500 Internal Server Error` - Application errors
- `503 Service Unavailable` - External service failures

## Security Considerations

### CSRF Protection
All POST requests require CSRF tokens:
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Authentication Requirements
Protected URLs require login:
```python
@login_required
def protected_view(request):
    # View code
```

### Permission Checks
Some URLs have additional permission requirements:
```python
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
```

## URL Testing Examples

### Manual Testing URLs
```bash
# Test challenge list
curl -H "Accept: text/html" https://boost-dev.herokuapp.com/challenges/

# Test challenge detail
curl -H "Accept: text/html" https://boost-dev.herokuapp.com/challenges/1/

# Test authentication required
curl -H "Accept: text/html" https://boost-dev.herokuapp.com/dashboard/
```

### Unit Test URL Patterns
```python
from django.test import TestCase
from django.urls import reverse

class URLTestCase(TestCase):
    def test_challenge_urls(self):
        # Test challenge list
        url = reverse('challenges')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Test challenge detail
        url = reverse('challenge_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        # Assert response
```

## Development and Production URL Differences

### Development URLs
```
http://127.0.0.1:8000/challenges/
http://localhost:8000/dashboard/
```

### Production URLs
```
https://boost-dev-9ed56bf6f182.herokuapp.com/challenges/
https://your-custom-domain.com/dashboard/
```

### Environment-Specific Settings
```python
# settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if not DEBUG:
    ALLOWED_HOSTS += ['.herokuapp.com', 'your-domain.com']
```

## URL Migration and Versioning

### Future API Versioning
```python
# Future API patterns
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
]
```

### Backward Compatibility
```python
# Redirect old URLs to new ones
urlpatterns = [
    path('old-challenges/', RedirectView.as_view(url='/challenges/', permanent=True)),
]
```

This comprehensive URL reference provides complete coverage of all routes, patterns, and API endpoints in the Boost.dev application, serving as a quick reference for developers working with the application's URL structure.
