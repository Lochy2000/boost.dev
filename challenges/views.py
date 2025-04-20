from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Challenge, ChallengeSolution, QuoteSubmission
from .forms import ChallengeForm, ChallengeSolutionForm
from services.ai_challenge import get_challenge_feedback, generate_new_challenge

@login_required
def challenge_list(request):
    """View for listing all challenges"""
    # Get filter parameters
    difficulty = request.GET.get('difficulty', '')
    
    # Get challenges from database
    challenges = Challenge.objects.filter(is_approved=True)
    
    # Apply difficulty filter if specified
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)
    
    context = {
        'challenges': challenges,
        'difficulty_filter': difficulty,
    }
    
    return render(request, 'challenges/view_challenges.html', context)

@login_required
def challenge_detail(request, pk):
    """View for displaying a single challenge"""
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    
    # Check if user has already submitted a solution
    user_solution = None
    if request.user.is_authenticated:
        user_solution = ChallengeSolution.objects.filter(
            challenge=challenge,
            user=request.user
        ).order_by('-submitted_at').first()
    
    # Create solution form
    form = ChallengeSolutionForm()
    
    context = {
        'challenge': challenge,
        'user_solution': user_solution,
        'form': form,
    }
    
    return render(request, 'challenges/challenge_detail.html', context)

@login_required
def create_challenge(request):
    """View for creating a new challenge"""
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user
            challenge.is_approved = True
            challenge.save()
            
            messages.success(request, "Your challenge has been created!")
            return redirect('challenge_detail', pk=challenge.pk)
    else:
        form = ChallengeForm()
    
    return render(request, 'challenges/create_challenge.html', {'form': form})

@login_required
def quote_list(request):
    """View for listing quotes (temporary until quotes are integrated with dashboard)"""
    # For now, just redirect to dashboard
    return render(request, 'dashboard/dashboard.html')

@login_required
def submit_solution(request, pk):
    """Submit a solution to a challenge and get AI feedback"""
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    
    if request.method == 'POST':
        form = ChallengeSolutionForm(request.POST)
        if form.is_valid():
            try:
                # Create the solution object
                solution = form.save(commit=False)
                solution.challenge = challenge
                solution.user = request.user
                
                # Get AI feedback
                try:
                    print(f"Getting AI feedback for challenge solution: {solution.solution_text[:100]}...")
                    solution.ai_feedback = get_challenge_feedback(
                        solution.solution_text, 
                        challenge, 
                        request.user.username
                    )
                    print(f"Received AI feedback: {solution.ai_feedback[:100]}...")
                except Exception as e:
                    print(f"Error getting AI feedback: {e}")
                    solution.ai_feedback = f"Our AI assistant is taking a break, but your solution shows real effort, {request.user.username}! Keep exploring different approaches and don't give up."
                
                solution.save()
                messages.success(request, "Your solution has been submitted! Check out the AI feedback.")
            except Exception as e:
                print(f"Error saving solution: {e}")
                messages.error(request, "There was an error saving your solution. Please try again.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    
    return redirect('challenge_detail', pk=pk)

@login_required
def generate_ai_challenge(request):
    """Generate a challenge using AI"""
    if request.method == 'POST':
        difficulty = request.POST.get('difficulty', 'beginner')
        topic = request.POST.get('topic', 'programming')
        
        try:
            # Get AI-generated challenge
            challenge_text = generate_new_challenge(difficulty, topic, request.user.username)
            
            # Parse the response (assuming it follows the format in our prompt)
            lines = challenge_text.strip().split('\n')
            
            title = ""
            description = ""
            hints = []
            
            current_section = None
            
            for line in lines:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                    current_section = "title"
                elif line.startswith("DESCRIPTION:"):
                    current_section = "description"
                elif line.startswith("HINTS:"):
                    current_section = "hints"
                elif current_section == "description" and line:
                    description += line + "\n"
                elif current_section == "hints" and line and not line.startswith("HINT"):
                    if line.strip() and not line.startswith("-"):
                        hints.append(line.strip())
            
            # Create the challenge
            challenge = Challenge(
                title=title if title else "AI Generated Challenge",
                description=description.strip(),
                difficulty=difficulty,
                hints=hints,
                created_by=request.user,
                is_ai_generated=True,
                is_approved=True  # Auto-approve AI challenges
            )
            challenge.save()
            
            messages.success(request, "Your AI challenge has been generated!")
            return redirect('challenge_detail', pk=challenge.pk)
        except Exception as e:
            print(f"Error generating AI challenge: {e}")
            messages.error(request, "There was an error generating your challenge. Please try again.")
    
    return render(request, 'challenges/generate_challenge.html')