from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DailyWin
from .forms import DailyWinForm
from services.ai_feedback import get_ai_feedback

from .models import DailyWin

@login_required
def submit_win(request):
    """View for submitting a new daily win"""
    if request.method == 'POST':
        form = DailyWinForm(request.POST)
        if form.is_valid():
            win = form.save(commit=False)
            win.user = request.user
            
            # Get AI feedback
            try:
                win.ai_feedback = get_ai_feedback(win.content)
            except Exception as e:
                print(f"Error getting AI feedback: {e}")
                win.ai_feedback = "Our AI assistant is taking a break, but your win is still amazing! Keep up the great work."
                
            win.save()
            messages.success(request, "Your win has been recorded! Check out the AI feedback.")
            return redirect('wins:view_win', win_id=win.id)
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
    
    return render(request, 'wins/view_win.html', {'win': win})

@login_required
def my_wins(request):
    """View for displaying the user's wins history"""
    wins = DailyWin.objects.filter(user=request.user)
    
    return render(request, 'wins/view_win.html', {'wins': wins})

@login_required
def toggle_public(request, win_id):
    """Toggle the public status of a win"""
    win = get_object_or_404(DailyWin, id=win_id, user=request.user)
    win.is_public = not win.is_public
    win.save()
    
    status = "public" if win.is_public else "private"
    messages.success(request, f"Your win is now {status}.")
    
    return redirect('wins:view_win', win_id=win.id)

def community_wins(request):
    """View for displaying public wins from all users"""
    wins = DailyWin.objects.filter(is_public=True)
    return render(request, 'wins/community_wins.html', {'wins': wins})

