. Test migrations locally
python manage.py migrate

# 3. Deploy to staging
git push staging main
heroku run python manage.py migrate -a your-staging-app

# 4. Test on staging environment

# 5. Deploy to production
git push heroku main
heroku run python manage.py migrate -a your-production-app
```

#### Backup Before Migration
```bash
# Create database backup
heroku pg:backups:capture -a your-app-name

# Download backup
heroku pg:backups:download -a your-app-name

# Restore backup if needed
heroku pg:backups:restore backup-url DATABASE_URL -a your-app-name
```

### 3. Data Migration Scripts

#### Custom Management Command
```python
# management/commands/migrate_user_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProgress, Achievement

class Command(BaseCommand):
    help = 'Migrate user data for new features'

    def handle(self, *args, **options):
        self.stdout.write('Starting data migration...')
        
        # Create progress for users without it
        users_without_progress = User.objects.filter(progress__isnull=True)
        for user in users_without_progress:
            UserProgress.objects.create(user=user)
            self.stdout.write(f'Created progress for {user.username}')
        
        # Award achievements retroactively
        rookie_achievement, created = Achievement.objects.get_or_create(
            name="Level 1 Rookie",
            defaults={'description': 'Welcome to Boost.dev!'}
        )
        
        for user in User.objects.all():
            if not user.achievements.filter(achievement=rookie_achievement).exists():
                user.achievements.create(achievement=rookie_achievement)
        
        self.stdout.write(self.style.SUCCESS('Data migration completed'))
```

Run migration:
```bash
python manage.py migrate_user_data
```

## Monitoring and Maintenance

### 1. Application Monitoring

#### Heroku Monitoring
```bash
# View logs
heroku logs --tail -a your-app-name

# Monitor performance
heroku metrics -a your-app-name

# Check dyno status
heroku ps -a your-app-name

# Restart application
heroku restart -a your-app-name
```

#### Error Tracking Setup
```python
# Install Sentry for error tracking
pip install sentry-sdk[django]

# Add to settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 2. Performance Monitoring

#### Database Performance
```python
# Add to settings.py for query monitoring
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

#### Response Time Monitoring
```python
# Custom middleware for timing
class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        response['X-Response-Time'] = f'{duration:.2f}s'
        return response
```

### 3. Backup and Recovery

#### Database Backup Strategy
```bash
# Schedule automatic backups (Heroku)
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles' -a your-app-name

# Manual backup
heroku pg:backups:capture -a your-app-name

# List backups
heroku pg:backups -a your-app-name

# Download backup
heroku pg:backups:download b001 -a your-app-name
```

#### Code Backup
```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Create release branches
git checkout -b release/v1.0.0
git push origin release/v1.0.0
```

## Security Deployment Checklist

### 1. Security Headers

#### Django Security Settings
```python
# Production security settings
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Cookie security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
```

### 2. Environment Security

#### Secret Management
```bash
# Use strong secret keys
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Rotate secrets regularly
heroku config:set SECRET_KEY="new-secret-key" -a your-app-name

# Use separate keys for different environments
heroku config:set GEMINI_API_KEY="prod-key" -a your-production-app
heroku config:set GEMINI_API_KEY="dev-key" -a your-staging-app
```

#### Access Control
```bash
# Limit Heroku collaborators
heroku access -a your-app-name
heroku access:add user@example.com --permissions deploy -a your-app-name

# Use Heroku Teams for organization access
heroku teams:create your-team-name
heroku apps:transfer --to your-team-name your-app-name
```

## Troubleshooting Deployment Issues

### 1. Common Heroku Issues

#### Build Failures
```bash
# Check build logs
heroku logs --source app --dyno=run -a your-app-name

# Clear build cache
heroku plugins:install heroku-repo
heroku repo:purge_cache -a your-app-name

# Redeploy
git commit --allow-empty -m "Force redeploy"
git push heroku main
```

#### Database Connection Issues
```python
# Test database connection
heroku run python manage.py dbshell -a your-app-name

# Check database config
heroku pg:info -a your-app-name

# Reset database (development only)
heroku pg:reset DATABASE_URL -a your-app-name
heroku run python manage.py migrate -a your-app-name
```

#### Static Files Issues
```bash
# Debug static files
heroku run python manage.py collectstatic --dry-run -a your-app-name

# Check WhiteNoise configuration
heroku run python -c "import whitenoise; print(whitenoise.__version__)" -a your-app-name

# Force static file collection
heroku run python manage.py collectstatic --clear --noinput -a your-app-name
```

### 2. Performance Issues

#### Memory Usage
```bash
# Monitor memory usage
heroku logs --ps web --source app -a your-app-name | grep "sample#memory"

# Scale to larger dynos if needed
heroku ps:scale web=1:standard-1x -a your-app-name
```

#### Database Performance
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check database connections
SELECT count(*) FROM pg_stat_activity;
```

### 3. SSL/TLS Issues

#### Certificate Problems
```bash
# Check SSL status
heroku certs -a your-app-name

# Add custom domain
heroku domains:add www.yourdomain.com -a your-app-name

# Check DNS configuration
dig www.yourdomain.com
```

## Rollback Procedures

### 1. Application Rollback

#### Quick Rollback
```bash
# Rollback to previous release
heroku rollback -a your-app-name

# Rollback to specific version
heroku releases -a your-app-name
heroku rollback v42 -a your-app-name
```

#### Database Rollback
```bash
# Create backup before rollback
heroku pg:backups:capture -a your-app-name

# Restore from backup
heroku pg:backups:restore b001 DATABASE_URL -a your-app-name

# Run necessary migrations
heroku run python manage.py migrate -a your-app-name
```

### 2. Emergency Procedures

#### Maintenance Mode
```bash
# Enable maintenance mode
heroku maintenance:on -a your-app-name

# Disable maintenance mode
heroku maintenance:off -a your-app-name
```

#### Scale Down
```bash
# Scale down to prevent damage
heroku ps:scale web=0 -a your-app-name

# Scale back up when ready
heroku ps:scale web=1 -a your-app-name
```

## Post-Deployment Verification

### 1. Functional Testing

#### Health Check Endpoints
```python
# Add health check view
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Simple health check endpoint."""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
```

#### Smoke Tests
```bash
# Test key endpoints
curl https://your-app.herokuapp.com/
curl https://your-app.herokuapp.com/health/
curl https://your-app.herokuapp.com/login/

# Test API endpoints (if any)
curl -H "Accept: application/json" https://your-app.herokuapp.com/api/challenges/
```

### 2. Performance Verification

#### Load Testing
```bash
# Simple load test with curl
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code} %{time_total}\n" https://your-app.herokuapp.com/
done

# Use more sophisticated tools
npm install -g loadtest
loadtest -n 100 -c 10 https://your-app.herokuapp.com/
```

### 3. Monitoring Setup Verification

#### Log Monitoring
```bash
# Check application logs
heroku logs --tail -a your-app-name

# Check for errors
heroku logs --source app | grep ERROR
```

#### Metrics Verification
```bash
# Check dyno metrics
heroku ps -a your-app-name

# Monitor response times
heroku logs --source router | grep "service="
```

This comprehensive deployment guide covers all aspects of deploying and maintaining the Boost.dev application across different platforms, with emphasis on security, monitoring, and reliability.
