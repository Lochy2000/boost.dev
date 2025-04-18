from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    content = models.TextField()
    summary = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    read_time = models.IntegerField(default=5)  # in minutes
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('dashboard:article_detail', kwargs={'slug': self.slug})
        
    def get_tags_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    github_url = models.URLField()
    demo_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    technologies = models.CharField(max_length=255, blank=True)  # Comma-separated list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-stars', '-created_at']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('dashboard:project_detail', kwargs={'slug': self.slug})
        
    def get_technologies_list(self):
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',')]

class ProjectFeedback(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'user']
    
    def __str__(self):
        return f"Feedback on {self.project.title} by {self.user.username}"

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('tutorial', 'Tutorial'),
        ('tool', 'Tool'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('course', 'Course'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    url = models.URLField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resources')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('dashboard:resource_detail', kwargs={'slug': self.slug})
        
    def get_tags_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]