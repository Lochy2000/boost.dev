from django.db import migrations, models

def set_default_correctness_level(apps, schema_editor):
    ChallengeSolution = apps.get_model('challenges', 'ChallengeSolution')
    for solution in ChallengeSolution.objects.all():
        if solution.is_correct and (not hasattr(solution, 'correctness_level') or not solution.correctness_level):
            solution.correctness_level = 'correct'
        elif not hasattr(solution, 'correctness_level') or not solution.correctness_level:
            solution.correctness_level = 'incorrect'
        solution.save()

class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),  # Adjust this to the latest migration number
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='challenges_challengesolution' 
                              AND column_name='correctness_level') THEN
                    ALTER TABLE challenges_challengesolution 
                    ADD COLUMN correctness_level character varying(20) DEFAULT 'correct';
                END IF;
            END
            $$;
            ''',
            reverse_sql='',
        ),
        migrations.RunPython(set_default_correctness_level),
    ]