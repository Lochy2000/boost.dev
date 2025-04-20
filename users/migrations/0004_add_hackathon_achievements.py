from django.db import migrations

def create_hackathon_achievements(apps, schema_editor):
    Achievement = apps.get_model('users', 'achievement')
    
    # Hackathon specific achievements
    hackathon_achievements = [
        {
            'name': 'Hackathon Hero',
            'description': 'Participated in the Boost.dev hackathon and tried out the achievements system!',
            'icon': 'medal',
        },
        {
            'name': 'Early Adopter',
            'description': 'Among the first to test the Boost.dev progress system',
            'icon': 'rocket',
        },
        {
            'name': 'Fast Learner',
            'description': 'Quickly progressed through the levels during testing',
            'icon': 'bolt',
        }
    ]
    
    # Create all achievements
    for achievement_data in hackathon_achievements:
        Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults={
                'description': achievement_data['description'],
                'icon': achievement_data['icon'],
            }
        )

def remove_hackathon_achievements(apps, schema_editor):
    Achievement = apps.get_model('users', 'achievement')
    Achievement.objects.filter(name__in=[
        'Hackathon Hero',
        'Early Adopter',
        'Fast Learner'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_add_initial_achievements'),
    ]

    operations = [
        migrations.RunPython(create_hackathon_achievements, remove_hackathon_achievements),
    ]