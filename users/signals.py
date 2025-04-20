from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from wins.models import DailyWin
from challenges.models import Challenge, ChallengeSolution
from .models import UserProgress, Achievement, UserAchievement
from .utils import add_user_points, award_level_achievement, award_achievement

# User registration signal already in models.py

@receiver(post_save, sender=DailyWin)
def update_progress_on_win(sender, instance, created, **kwargs):
    """Add points when user logs a win"""
    if created:
        # Add points for creating a win
        leveled_up, _, level = add_user_points(instance.user, 20, "Logged a win!")
        
        # Check if this is the user's first win
        win_count = DailyWin.objects.filter(user=instance.user).count()
        if win_count == 1:
            # Award First Win achievement
            award_achievement(instance.user, "First Win")
        
        if leveled_up:
            # Award level achievement
            award_level_achievement(instance.user, level)

@receiver(post_save, sender=ChallengeSolution)
def update_progress_on_challenge_complete(sender, instance, created, **kwargs):
    """Add points when user completes a challenge"""
    if instance.is_correct:
        # Add points based on difficulty
        if instance.challenge.difficulty == 'beginner':
            points = 30
        elif instance.challenge.difficulty == 'intermediate':
            points = 45
        else:  # Hard
            points = 60
        
        reason = f"Completed {instance.challenge.difficulty} challenge!"
        leveled_up, _, level = add_user_points(instance.user, points, reason)
        
        # Check if this is the user's first challenge solution
        solution_count = ChallengeSolution.objects.filter(user=instance.user, is_correct=True).count()
        if solution_count == 1:
            # Award Challenge Accepted achievement
            award_achievement(instance.user, "Challenge Accepted")
        
        if leveled_up:
            # Award level achievement
            award_level_achievement(instance.user, level)

@receiver(post_save, sender=Challenge)
def update_progress_on_challenge_creation(sender, instance, created, **kwargs):
    """Add points when user creates a challenge"""
    if created:
        # Add points for creating a challenge
        leveled_up, _, level = add_user_points(instance.created_by, 40, "Created a challenge!")
        
        # Check if this is the user's first challenge creation
        challenge_count = Challenge.objects.filter(created_by=instance.created_by).count()
        if challenge_count == 1:
            # Award Challenge Creator achievement
            award_achievement(instance.created_by, "Challenge Creator")
        
        if leveled_up:
            # Award level achievement
            award_level_achievement(instance.created_by, level)