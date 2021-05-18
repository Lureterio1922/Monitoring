import os

from celery import Celery

from clients.views import check_status

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Monitoring.settings')

app = Celery('Monitoring')

app.config_from_object('django.conf:settings',  namespace='CELERY')


@app.task
def check_status_server():
    print("Background task started...")
    check_status(None)



app.conf.beat_schedule = {
    'poll-every-minute': {
        'task': 'Monitoring.celery.check_status_server',
        'schedule': 60,
        'options': {
            'expires': 120
        }
    }
}