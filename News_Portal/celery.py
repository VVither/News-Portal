import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')
 
app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'send_weekly_email': {
        'task': 'news.tasks.send_weekly_email',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # В понедельник в 8:00
    },
}