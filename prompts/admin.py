from django.contrib import admin
from .models import Quote, Challenge, DailyPrompt

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text_snippet', 'author', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('text', 'author')
    
    def text_snippet(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_snippet.short_description = 'Quote'

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(DailyPrompt)
class DailyPromptAdmin(admin.ModelAdmin):
    list_display = ('date', 'quote', 'challenge')
    list_filter = ('date',)
    search_fields = ('quote__text', 'challenge__title')
