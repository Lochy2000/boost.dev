from django import forms
from .models import ProjectFeedback

class ProjectFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProjectFeedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'rows': 3,
                'placeholder': 'Share your thoughts on this project...'
            }),
            'rating': forms.Select(attrs={
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 p-2'
            })
        }
        labels = {
            'comment': 'Your Feedback',
            'rating': 'Rating (1-5)'
        }