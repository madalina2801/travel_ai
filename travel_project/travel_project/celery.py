import os
from celery import Celery

# Set Django settings BEFORE anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_project.settings')

app = Celery('travel_project')

# Pull config from Django settings, namespace CELERY_ to avoid collisions
app.config_from_object('django.conf:settings', namespace='CELERY')

# Disable connection pooling — forces a fresh connection every time
# This prevents stale connections initialized before settings were loaded
app.conf.broker_pool_limit = None

# Auto-discover tasks.py in every INSTALLED_APP
app.autodiscover_tasks()