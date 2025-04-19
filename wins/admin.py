
from django.contrib import admin
from .models import DailyWin

@admin.register(DailyWin)
class DailyWinAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_content', 'is_public', 'created_at', 'has_ai_feedback')
    list_filter = ('is_public', 'created_at')
    search_fields = ('user__username', 'content', 'ai_feedback')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Win Summary'

    def has_ai_feedback(self, obj):
        return bool(obj.ai_feedback.strip())
    has_ai_feedback.boolean = True
    has_ai_feedback.short_description = 'AI Feedback?'