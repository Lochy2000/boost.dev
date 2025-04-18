from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def submission_list(request):
    """View for listing all submissions from the current user"""
    return render(request, 'dashboard/dashboard.html')  # Temporary redirect

@login_required
def new_submission(request):
    """View for creating a new submission"""
    return render(request, 'dashboard/dashboard.html')  # Temporary redirect