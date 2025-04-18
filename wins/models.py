from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyWin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_wins')
    content = models.TextField()
    ai_feedback = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s win on {self.created_at.strftime('%Y-%m-%d')}"
        
    def is_today(self):
        return self.created_at.date() == timezone.now().date()