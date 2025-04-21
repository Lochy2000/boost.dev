from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import DailyWin
from .forms import DailyWinForm
from services.ai_feedback import get_ai_feedback
from challenges.models import ChallengeSolution

@login_required
def submit_win(request):
    """View for submitting a new daily win"""
    if request.method == 'POST':
        form = DailyWinForm(request.POST)
        if form.is_valid():
            try:
                win = form.save(commit=False)
                win.user = request.user
                
                # Get AI feedback with username
                try:
                    print(f"Getting AI feedback for: {win.content}")
                    feedback = get_ai_feedback(win.content, request.user.username)
                    # Replace the template placeholder with actual username
                    win.ai_feedback = feedback.replace("{user.username}", request.user.username)
                    print(f"Received AI feedback: {win.ai_feedback}")
                except Exception as e:
                    print(f"Error getting AI feedback: {e}")
                    win.ai_feedback = f"Our AI assistant is taking a break, but your win is still amazing, {request.user.username}! Keep up the great work."
                    
                win.save()
                messages.success(request, "Your win has been recorded! Check out the AI feedback.")
                return redirect('wins:view_win', win_id=win.id)
            except Exception as e:
                print(f"Error saving win: {e}")
                messages.error(request, "There was an error saving your win. Please try again.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DailyWinForm()
    
    return render(request, 'wins/submit_win.html', {'form': form})

@login_required
def view_win(request, win_id):
    """View for displaying a single win with AI feedback"""
    win = get_object_or_404(DailyWin, id=win_id)
    
    # Only allow the win owner to see it unless it's public
    if win.user != request.user and not win.is_public:
        messages.error(request, "You don't have permission to view this win.")
        return redirect('dashboard')
    
    # Create a list containing just this win for the template
    wins = [win]
    
    # Check if user has already submitted a win today
    has_win_today = DailyWin.objects.filter(
        user=request.user, 
        created_at__date=timezone.now().date()
    ).exists()
    
    return render(request, 'wins/view_win.html', {
        'wins': wins,
        'has_win_today': has_win_today
    })

@login_required
def my_wins(request):
    """View for displaying the user's wins history"""
    wins = DailyWin.objects.filter(user=request.user).order_by('-created_at')
    # Get all user's challenge solutions
    challenge_solutions = ChallengeSolution.objects.filter(user=request.user).order_by('-submitted_at')
    
    # Check if user has already submitted a win today
    has_win_today = DailyWin.objects.filter(
        user=request.user, 
        created_at__date=timezone.now().date()
    ).exists()
    
    return render(request, 'wins/wins_list.html', {
        'wins': wins,
        'challenge_solutions': challenge_solutions,
        'has_win_today': has_win_today
    })

@login_required
def toggle_public(request, win_id):
    """Toggle the public status of a win"""
    win = get_object_or_404(DailyWin, id=win_id, user=request.user)
    win.is_public = not win.is_public
    win.save()
    
    status = "public" if win.is_public else "private"
    messages.success(request, f"Your win is now {status}.")
    
    return redirect('wins:view_win', win_id=win.id)

@require_POST
@login_required
def toggle_celebration(request, win_id):
    """Toggle celebration for a win"""
    win = get_object_or_404(DailyWin, id=win_id)
    
    # Toggle the celebration
    was_added = win.toggle_celebration(request.user)
    
    # Create notification for the win owner if celebration was added
    if was_added and win.user != request.user:
        from users.models import Notification
        Notification.objects.create(
            user=win.user,
            notification_type='celebration',
            content=f"{request.user.username} celebrated your win!",
            link=f'/wins/view/{win.id}/'
        )
    
    return JsonResponse({
        'success': True,
        'celebration_count': win.celebration_count(),
        'is_celebrated': was_added
    })

def community_wins(request):
    """View for displaying public wins from all users"""
    wins = DailyWin.objects.filter(is_public=True).order_by('-created_at')
    
    # Add celebration info for each win
    for win in wins:
        win.celebration_count = win.celebration_count()
        if request.user.is_authenticated:
            win.is_celebrated_by_user = win.is_celebrated_by(request.user)
    
    # Get all challenge solutions, not just the ones marked as correct
    challenge_solutions = ChallengeSolution.objects.all().order_by('-submitted_at')
    
    # Check if user has already submitted a win today (if authenticated)
    has_win_today = False
    if request.user.is_authenticated:
        has_win_today = DailyWin.objects.filter(
            user=request.user, 
            created_at__date=timezone.now().date()
        ).exists()
    
    return render(request, 'wins/community_wins.html', {
        'wins': wins,
        'challenge_solutions': challenge_solutions,
        'has_win_today': has_win_today
    })
