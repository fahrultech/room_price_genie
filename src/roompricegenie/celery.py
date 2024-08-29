from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roompricegenie.settings')

app = Celery('roompricegenie')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-event-every-five-minute': {
        'task': 'data_provider.tasks.add_event_to_data_provider',
        'schedule': crontab(minute='*/5'),  # Runs every 5 minutes
    },
    'populate-dashboard-ten-minute': {
        'task': 'dashboard.tasks.populate_dashboard_service',
        'schedule': crontab(minute='*/15'),  # Runs every 15 minutes 
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))