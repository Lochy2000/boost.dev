from django.core.management.base import BaseCommand
from users.models import Achievement

class Command(BaseCommand):
    help = 'Initialize the achievement system with default level-up achievements'

    def handle(self, *args, **options):
        # Create level-up achievements
        level_achievements = [
            {
                'name': 'Level 1 Rookie',
                'description': 'Started your journey with Boost.dev!',
                'icon': 'seedling',
            },
            {
                'name': 'Level 2 Explorer',
                'description': "You've reached level 2! You're making progress.",
                'icon': 'compass',
            },
            {
                'name': 'Level 3 Hacker',
                'description': "Level 3 achieved! You're getting serious.",
                'icon': 'code',
            },
            {
                'name': 'Level 4 Wizard',
                'description': 'Level 4! Your skills are impressive.',
                'icon': 'hat-wizard',
            },
            {
                'name': 'Level 5 Master',
                'description': "You've reached the highest level! True mastery achieved.",
                'icon': 'crown',
            },
        ]
        
        for achievement_data in level_achievements:
            Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults={
                    'description': achievement_data['description'],
                    'icon': achievement_data['icon'],
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully initialized level-up achievements'))