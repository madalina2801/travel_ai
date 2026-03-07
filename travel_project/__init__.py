# This ensures the Celery app is loaded when Django starts,
# so @shared_task decorators are registered correctly.
from .celery import app as celery_app

__all__ = ('celery_app',)
