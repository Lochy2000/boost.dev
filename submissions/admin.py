from django.contrib import admin
from .models import QuoteSubmission, ChallengeSubmission

@admin.register(QuoteSubmission)
class QuoteSubmissionAdmin(admin.ModelAdmin):
    list_display = ('text_snippet', 'author', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('text', 'author', 'user__username')
    ordering = ('-created_at',)

    def text_snippet(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_snippet.short_description = 'Quote'


@admin.register(ChallengeSubmission)
class ChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'is_approved', 'created_at')
    list_filter = ('difficulty', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)