from django import forms
from .models import Challenge, ChallengeSolution, QuoteSubmission

class ChallengeForm(forms.ModelForm):
    """Form for creating a new challenge"""
    # Add multiple hint fields
    hint1 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'}))
    hint2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'}))
    hint3 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'}))
    
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'w-full bg-gray-800 border border-gray-700 rounded py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'difficulty': forms.RadioSelect()
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convert individual hint fields to a JSON field
        hints = []
        if self.cleaned_data.get('hint1'):
            hints.append(self.cleaned_data.get('hint1'))
        if self.cleaned_data.get('hint2'):
            hints.append(self.cleaned_data.get('hint2'))
        if self.cleaned_data.get('hint3'):
            hints.append(self.cleaned_data.get('hint3'))
        
        # Make sure we have at least one hint
        if not hints:
            hints.append("Start by breaking down the problem into smaller parts.")
            
        instance.hints = hints
        
        if commit:
            instance.save()
        return instance

class ChallengeSolutionForm(forms.ModelForm):
    """Form for submitting a solution to a challenge"""
    class Meta:
        model = ChallengeSolution
        fields = ['solution_text']
        widgets = {
            'solution_text': forms.Textarea(attrs={'rows': 8, 'class': 'w-full bg-gray-800 text-white p-3 rounded resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500'})
        }

class QuoteSubmissionForm(forms.ModelForm):
    """Form for submitting a quote"""
    class Meta:
        model = QuoteSubmission
        fields = ['text', 'author']