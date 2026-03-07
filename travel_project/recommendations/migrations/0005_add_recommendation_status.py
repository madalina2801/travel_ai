from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0004_remove_recommendation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('pending',   'Pending'),
                    ('completed', 'Completed'),
                    ('failed',    'Failed'),
                ],
                default='completed',
            ),
        ),
    ]