from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    avatar = models.URLField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

# Signal to create user profile and progress when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserProgress.objects.create(user=instance)
        
        # Award Level 1 achievement
        try:
            rookie_achievement = Achievement.objects.get(name="Level 1 Rookie")
            UserAchievement.objects.create(user=instance, achievement=rookie_achievement)
        except Achievement.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    next_level_threshold = models.IntegerField(default=100)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Progress - Level {self.level}"
    
    def calculate_percentage(self):
        """Calculate percentage progress to next level"""
        if self.level == 1:
            previous_level_points = 0
        elif self.level == 2:
            previous_level_points = 30
        elif self.level == 3:
            previous_level_points = 70
        elif self.level == 4:
            previous_level_points = 120
        else:  # level 5
            previous_level_points = 200
        
        points_in_current_level = self.points - previous_level_points
        points_needed_for_next = self.next_level_threshold - previous_level_points
        
        if self.level >= 5:  # Max level
            return 100
        
        return min(int((points_in_current_level / points_needed_for_next) * 100), 100)
    
    def update_level(self):
        """Update user level based on points"""
        previous_level = self.level
        
        # Hackathon demo version - faster level progression
        if self.points < 30:
            self.level = 1
            self.next_level_threshold = 30
        elif self.points < 70:
            self.level = 2
            self.next_level_threshold = 70
        elif self.points < 120:
            self.level = 3
            self.next_level_threshold = 120
        elif self.points < 200:
            self.level = 4
            self.next_level_threshold = 200
        else:
            self.level = 5
            self.next_level_threshold = 200  # Max level
        
        self.save()
        return self.level > previous_level  # Return True if leveled up
    
    def add_points(self, points):
        """Add points and update level if necessary"""
        self.points += points
        leveled_up = self.update_level()
        return leveled_up
    
    def get_level_color(self):
        """Returns color class for the level"""
        colors = {
            1: 'blue',
            2: 'green',
            3: 'yellow',
            4: 'orange',
            5: 'purple'
        }
        return colors.get(self.level, 'blue')


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='trophy')  # Font Awesome icon name
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        
    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"
