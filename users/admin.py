from django.contrib import admin
from .models import UserProfile, UserProgress, Achievement, UserAchievement

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_level', 'joined_at')
    search_fields = ('user__username', 'bio')
    list_filter = ('experience_level',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'level', 'next_level_threshold', 'last_updated')
    search_fields = ('user__username',)
    list_filter = ('level',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon')
    search_fields = ('name', 'description')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    search_fields = ('user__username', 'achievement__name')
    list_filter = ('achievement', 'earned_at')
