from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Challenge, ChallengeSolution, QuoteSubmission
from .forms import ChallengeForm, ChallengeSolutionForm
from services.ai_challenge import get_challenge_feedback, generate_new_challenge

@login_required
def view_challenge_solutions(request, pk):
    """View for displaying all solutions for a specific challenge"""
    challenge = get_object_or_404(Challenge, pk=pk, is_approved=True)
    
    # Get all solutions for this challenge
    solutions = ChallengeSolution.objects.filter(
        challenge=challenge,
        is_correct=True
    ).select_related('user', 'user__userprofile').order_by('-submitted_at')
    
    context = {
        'challenge': challenge,
        'solutions': solutions,
    }
    
    return render(request, 'challenges/challenge_solutions.html', context)

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
    
    # Get solutions from other users
    other_solutions = ChallengeSolution.objects.filter(
        challenge=challenge,
        is_correct=True
    ).exclude(
        user=request.user
    ).select_related('user', 'user__userprofile').order_by('-submitted_at')[:5]
    
    # Create solution form
    form = ChallengeSolutionForm()
    
    context = {
        'challenge': challenge,
        'user_solution': user_solution,
        'other_solutions': other_solutions,
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
                # Check if update or create new solution
                update_existing = request.POST.get('update_existing') == 'true'
                
                # If updating existing solution, get the most recent one
                if update_existing:
                    solution = ChallengeSolution.objects.filter(
                        challenge=challenge,
                        user=request.user
                    ).order_by('-submitted_at').first()
                    
                    # If somehow we don't find one (shouldn't happen), create new
                    if not solution:
                        solution = ChallengeSolution()
                        solution.challenge = challenge
                        solution.user = request.user
                else:
                    # Create a new solution
                    solution = ChallengeSolution()
                    solution.challenge = challenge
                    solution.user = request.user
                
                # Update the solution text from the form
                solution.solution_text = form.cleaned_data['solution_text']
                solution.is_correct = True  # Default to marking as correct
                
                # Get AI feedback
                try:
                    print(f"Getting AI feedback for challenge solution: {solution.solution_text[:100]}...")
                    solution.ai_feedback = get_challenge_feedback(
                        solution.solution_text, 
                        challenge, 
                        request.user.username
                    )
                    print(f"Received AI feedback: {solution.ai_feedback[:100]}...")
                    
                    # Determine correctness level based on the AI feedback
                    feedback_lower = solution.ai_feedback.lower()
                    if any(phrase in feedback_lower for phrase in ['perfect', 'excellent', 'great job', 'fantastic']):
                        solution.correctness_level = 'correct'
                    elif any(phrase in feedback_lower for phrase in ['almost there', 'very close', 'nearly']):
                        solution.correctness_level = 'almost'
                    elif any(phrase in feedback_lower for phrase in ['good attempt', 'on the right track', 'making progress']):
                        solution.correctness_level = 'partial'
                    elif any(phrase in feedback_lower for phrase in ['consider trying', 'you might want to', 'not quite']):
                        solution.correctness_level = 'incorrect'
                    else:
                        solution.correctness_level = 'correct'  # Default if we can't determine
                        
                except Exception as e:
                    print(f"Error getting AI feedback: {e}")
                    solution.ai_feedback = f"Our AI assistant is taking a break, but your solution shows real effort, {request.user.username}! Keep exploring different approaches and don't give up."
                    solution.correctness_level = 'partial'  # Default when AI feedback fails
                
                solution.save()
                
                if update_existing:
                    messages.success(request, "Your solution has been updated! Check out the new AI feedback.")
                else:
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
            
            # Parse the response with improved structured parsing
            lines = challenge_text.strip().split('\n')
            
            title = ""
            description = ""
            hints = []
            
            current_section = None
            
            # Improved parsing with specific hint headers
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                    current_section = "title"
                elif line.startswith("DESCRIPTION:"):
                    current_section = "description"
                elif line.startswith("HINT 1:"):
                    hint = line.replace("HINT 1:", "").strip()
                    if hint:  # Only add non-empty hints
                        hints.append(hint)
                    current_section = "hint1"
                elif line.startswith("HINT 2:"):
                    hint = line.replace("HINT 2:", "").strip()
                    if hint:  # Only add non-empty hints
                        hints.append(hint)
                    current_section = "hint2"
                elif line.startswith("HINT 3:"):
                    hint = line.replace("HINT 3:", "").strip()
                    if hint:  # Only add non-empty hints
                        hints.append(hint)
                    current_section = "hint3"
                # Legacy support for old format
                elif line.startswith("HINTS:"):
                    current_section = "hints"  
                elif current_section == "description":
                    description += line + "\n"
                elif current_section == "hint1" and not line.startswith("HINT"):
                    # Append to existing hint if it's a continuation
                    if hints and len(hints) >= 1:
                        hints[0] += " " + line
                elif current_section == "hint2" and not line.startswith("HINT"):
                    if hints and len(hints) >= 2:
                        hints[1] += " " + line
                elif current_section == "hint3" and not line.startswith("HINT"):
                    if hints and len(hints) >= 3:
                        hints[2] += " " + line
                # Legacy support for old format
                elif current_section == "hints" and not line.startswith("HINT"):
                    if line.strip() and not line.startswith("-"):
                        hints.append(line.strip())
                        
            # Ensure we have exactly 3 hints with quality fallbacks
            default_hints = [
                "Start by breaking down the problem into smaller parts. What's the first step you would take?",
                "Consider edge cases and how your solution handles different inputs. What assumptions are you making?",
                "Look at your algorithm's efficiency. Can you optimize it further? Remember to test your solution with various inputs."
            ]
            
            # Add quality default hints if we don't have enough
            while len(hints) < 3:
                hints.append(default_hints[len(hints)])
                
            # Limit to 3 hints if we somehow got more
            hints = hints[:3]
            
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