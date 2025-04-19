from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    github_username = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': 'Your GitHub username (optional)'
        })
    )
    
    experience_level = forms.ChoiceField(
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        widget=forms.Select(attrs={
            'class': 'bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 p-2'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'github_username', 'experience_level']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Email address'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': 'Confirm password'
        })

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'github_username', 'experience_level', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-[#121212] text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#312fa6]',
                'rows': 3
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-[#121212] text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#312fa6]'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-[#121212] text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#312fa6]'
            }),
            'avatar': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 bg-[#121212] text-white border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#312fa6]'
            }),
        }