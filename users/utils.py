from django.contrib import messages
from .models import UserProgress, Achievement, UserAchievement

def add_user_points(user, points, reason=""):
    """
    Add points to user and check for level up
    Returns True if user leveled up
    """
    try:
        # Get or create user progress
        progress, created = UserProgress.objects.get_or_create(user=user)
        
        # Add points
        leveled_up = progress.add_points(points)
        
        if reason:
            message = f"{reason} +{points} points"
        else:
            message = f"+{points} points"
        
        return leveled_up, message, progress.level
    except Exception as e:
        print(f"Error adding points to user: {e}")
        return False, "", 0

def award_achievement(user, achievement_name, request=None):
    """Award achievement to user and show notification"""
    try:
        achievement = Achievement.objects.get(name=achievement_name)
        
        # Check if user already has this achievement
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            UserAchievement.objects.create(user=user, achievement=achievement)
            
            # Show notification message if request provided
            if request:
                messages.success(request, f"Achievement Unlocked: {achievement.name} - {achievement.description}")
            
            return True
    except Achievement.DoesNotExist:
        pass
    
    return False

def award_level_achievement(user, level, request=None):
    """Award level achievement to user"""
    achievement_name = f"Level {level} {get_level_title(level)}"
    awarded = award_achievement(user, achievement_name, request)
    
    # Hackathon demo - award Fast Learner achievement when reaching level 3
    if level >= 3:
        award_achievement(user, "Fast Learner", request)
        
    return awarded

def get_level_title(level):
    """Get title for level"""
    titles = {
        1: "Rookie",
        2: "Explorer",
        3: "Hacker",
        4: "Wizard",
        5: "Master"
    }
    return titles.get(level, "Unknown")