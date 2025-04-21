from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('hard', 'Hard')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    hints = models.JSONField(default=list)  # Store multiple hints
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    is_ai_generated = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
        
    def get_difficulty_color(self):
        """Returns a Tailwind CSS color class based on difficulty"""
        if self.difficulty == 'beginner':
            return 'green-600'
        elif self.difficulty == 'intermediate':
            return 'yellow-600'
        else:
            return 'red-600'

class ChallengeSolution(models.Model):
    CORRECTNESS_CHOICES = [
        ('correct', 'Correct'),
        ('almost', 'Almost Correct'),
        ('partial', 'Partially Correct'),
        ('incorrect', 'Not Quite Right')
    ]
    
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_solutions')
    solution_text = models.TextField()
    ai_feedback = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    correctness_level = models.CharField(max_length=20, choices=CORRECTNESS_CHOICES, default='correct')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s solution to {self.challenge.title}"
    
    def get_correctness_color(self):
        """Returns a Tailwind CSS color class based on correctness"""
        if self.correctness_level == 'correct':
            return 'green-600'
        elif self.correctness_level == 'almost':
            return 'yellow-500'
        elif self.correctness_level == 'partial':
            return 'orange-500'
        else:
            return 'red-500'

# Moving the QuoteSubmission model to challenges for now
# Later we'll move this functionality to integreate with prompts
class QuoteSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_quotes')
    text = models.TextField()
    author = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.text[:30]}... - {self.author}"