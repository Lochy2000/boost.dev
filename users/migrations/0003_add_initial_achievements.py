from django.db import migrations

def create_initial_achievements(apps, schema_editor):
    Achievement = apps.get_model('users', 'achievement')
    
    # Level achievements
    level_achievements = [
        {
            'name': 'Level 1 Rookie',
            'description': 'Started your journey with Boost.dev!',
            'icon': 'seedling',
        },
        {
            'name': 'Level 2 Explorer',
            'description': 'You\'ve reached level 2! You\'re making progress.',
            'icon': 'compass',
        },
        {
            'name': 'Level 3 Hacker',
            'description': 'Level 3 achieved! You\'re getting serious.',
            'icon': 'code',
        },
        {
            'name': 'Level 4 Wizard',
            'description': 'Level 4! Your skills are impressive.',
            'icon': 'hat-wizard',
        },
        {
            'name': 'Level 5 Master',
            'description': 'You\'ve reached the highest level! True mastery achieved.',
            'icon': 'crown',
        },
    ]
    
    # Action achievements
    action_achievements = [
        {
            'name': 'First Win',
            'description': 'Log your first win',
            'icon': 'trophy',
        },
        {
            'name': 'Challenge Accepted',
            'description': 'Complete your first challenge',
            'icon': 'check-circle',
        },
        {
            'name': 'Challenge Creator',
            'description': 'Create your first challenge',
            'icon': 'lightbulb',
        },
    ]
    
    # Create all achievements
    for achievement_data in level_achievements + action_achievements:
        Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults={
                'description': achievement_data['description'],
                'icon': achievement_data['icon'],
            }
        )

def remove_initial_achievements(apps, schema_editor):
    Achievement = apps.get_model('users', 'achievement')
    Achievement.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_progress_models'),
    ]

    operations = [
        migrations.RunPython(create_initial_achievements, remove_initial_achievements),
    ]