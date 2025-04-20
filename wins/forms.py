# wins/forms.py
from django import forms
from .models import DailyWin

class DailyWinForm(forms.ModelForm):
    """Form for submitting or editing a daily win"""
    
    class Meta:
        model = DailyWin
        fields = ['content', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'I finally figured out that tricky bug today...'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'mr-2 text-indigo-600 rounded'
            })
        }
        labels = {
            'content': 'What\'s one win you had today? (big or small)',
            'is_public': 'Share with community (others can see your win)'
        }
        help_texts = {
            'is_public': 'Sharing your wins can inspire others who might be facing similar challenges.'
        }