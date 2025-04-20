from django.utils import timezone
from .models import UserFlag

def user_progress(request):
    """
    Add user progress data to all templates
    """
    context = {
        'level_up_flag': None
    }
    
    if request.user.is_authenticated:
        try:
            # Add user progress data
            context.update({
                'user': request.user,
                'user_progress': request.user.progress,
                'level_color': request.user.progress.get_level_color(),
                'progress_percentage': request.user.progress.calculate_percentage()
            })
            
            # Check for level-up flags
            level_up_flag = UserFlag.objects.filter(
                user=request.user,
                flag_type='level_up',
                is_read=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if level_up_flag:
                context['level_up_flag'] = level_up_flag.value
                level_up_flag.is_read = True
                level_up_flag.save()
                
        except Exception as e:
            print(f"Error in user_progress context processor: {e}")
            # return empty values to avoid template errors
            context.update({
                'user_progress': None,
                'level_color': 'blue',
                'progress_percentage': 0
            })
    
    return context