from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import UserProgress, Achievement, UserAchievement
from .utils import add_user_points, award_level_achievement, award_achievement, get_level_title

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Set profile fields
            user.userprofile.github_username = form.cleaned_data.get('github_username')
            user.userprofile.experience_level = form.cleaned_data.get('experience_level')
            user.userprofile.save()
            
            # Log the user in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            # Award first level achievement
            award_level_achievement(user, 1)
            
            messages.success(request, "Registration successful!")
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = SignUpForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                
                # Hackathon demo - award special achievement when logging in
                try:
                    from .utils import award_achievement
                    award_achievement(user, "Hackathon Hero", request)
                    
                    # Add some points for logging in (demo only)
                    from .utils import add_user_points
                    add_user_points(user, 10, "Logged in during hackathon")
                except Exception as e:
                    print(f"Error awarding hackathon achievement: {e}")
                    
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            
            # Add points for updating profile
            leveled_up, points_message, new_level = add_user_points(request.user, 15, "Profile updated")
            
            if leveled_up:
                # Award achievement for new level
                award_level_achievement(request.user, new_level, request)
                messages.success(request, f"Congratulations! You've reached Level {new_level}!")
            
            # Hackathon demo - award Early Adopter achievement for profile updates
            award_achievement(request.user, "Early Adopter", request)
            
            messages.success(request, f"Profile updated successfully! {points_message}")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    # Get user achievements
    user_achievements = request.user.achievements.all().select_related('achievement')
    
    return render(request, 'users/profile.html', {
        'form': form,
        'user_achievements': user_achievements
    })

def social_auth_callback(request):
    """Handle callback from social authentication providers"""
    # This would be implemented based on the social auth library being used
    return redirect('dashboard:dashboard')