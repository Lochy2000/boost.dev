from django.db import models
from django.utils import timezone

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.text[:30]}... - {self.author}"

class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class DailyPrompt(models.Model):
    date = models.DateField(unique=True, default=timezone.now)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Prompt for {self.date.strftime('%Y-%m-%d')}"
    
    @classmethod
    def get_today(cls):
        today = timezone.now().date()
        
        # Check if we have active quotes and challenges
        active_quote = Quote.objects.filter(is_active=True).order_by('?').first()
        active_challenge = Challenge.objects.filter(is_active=True).order_by('?').first()
        
        # Create fallback objects if needed
        if not active_quote:
            active_quote = Quote.objects.create(
                text="The journey of a thousand miles begins with a single step.",
                author="Lao Tzu",
                is_active=True
            )
        
        if not active_challenge:
            active_challenge = Challenge.objects.create(
                title="Getting Started Challenge",
                description="Set up your development environment and commit your first code change.",
                difficulty="easy",
                is_active=True
            )
        
        # Now we can safely use get_or_create
        prompt, created = cls.objects.get_or_create(date=today, defaults={
            'quote': active_quote,
            'challenge': active_challenge
        })
        return prompt