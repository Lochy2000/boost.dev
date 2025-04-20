from django.contrib import admin
from .models import Challenge, ChallengeSolution, QuoteSubmission

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'difficulty', 'is_ai_generated', 'is_approved', 'created_at')
    list_filter = ('difficulty', 'is_approved', 'is_ai_generated', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    ordering = ('-created_at',)

@admin.register(ChallengeSolution)
class ChallengeSolutionAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'is_correct', 'submitted_at')
    list_filter = ('is_correct', 'submitted_at')
    search_fields = ('challenge__title', 'user__username', 'solution_text')
    ordering = ('-submitted_at',)

@admin.register(QuoteSubmission)
class QuoteSubmissionAdmin(admin.ModelAdmin):
    list_display = ('text_snippet', 'author', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('text', 'author', 'user__username')
    ordering = ('-created_at',)

    def text_snippet(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_snippet.short_description = 'Quote'