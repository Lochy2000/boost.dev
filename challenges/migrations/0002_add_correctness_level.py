from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('challenges', '0001_initial'),  # Update this with the actual previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='challengesolution',
            name='correctness_level',
            field=models.CharField(choices=[('correct', 'Correct'), ('almost', 'Almost Correct'), ('partial', 'Partially Correct'), ('incorrect', 'Not Quite Right')], default='correct', max_length=20),
        ),
    ]
