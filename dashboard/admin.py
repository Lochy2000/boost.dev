from django.contrib import admin
from .models import Article, Project, ProjectFeedback, Resource

# Admin for Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_featured', 'read_time', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username', 'tags')
    list_filter = ('is_featured', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}

# Admin for Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'stars', 'forks', 'views', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('title', 'owner__username', 'technologies')
    list_filter = ('is_featured', 'created_at', 'updated_at')
    ordering = ('-stars', '-created_at')
    prepopulated_fields = {'slug': ('title',)}

# Admin for ProjectFeedback
@admin.register(ProjectFeedback)
class ProjectFeedbackAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'rating', 'created_at')
    search_fields = ('project__title', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

# Admin for Resource
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at', 'created_by')
    search_fields = ('title', 'tags', 'category', 'created_by__username')
    list_filter = ('category', 'is_featured', 'created_at')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}

