def user_progress(request):
    """
    Add user progress data to all templates
    """
    if request.user.is_authenticated:
        try:
            # drectly uses  users oject to access progress - no need for the extra variables
            return {
                'user': request.user,
                # keeping these for backward compatibility
                'user_progress': request.user.progress,
                'level_color': request.user.progress.get_level_color(),
                'progress_percentage': request.user.progress.calculate_percentage()
            }
        except Exception as e:
            print(f"Error in user_progress context processor: {e}")
            # return empty values to avoid template errors
            return {
                'user_progress': None,
                'level_color': 'blue',
                'progress_percentage': 0
            }
    
    return {}