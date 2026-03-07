from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Adds a 'status' field to Recommendation to track async processing state.
    pending   → task published to RabbitMQ, worker not yet done
    completed → worker finished, all fields populated
    failed    → worker exhausted retries
    """

    dependencies = [
        ('recommendations', '0002_alter_recommendation_location_and_more'),
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
                default='completed',  # keeps all existing rows valid
            ),
        ),
    ]
