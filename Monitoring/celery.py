import os

from celery import Celery

from clients.views import check_status

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Monitoring.settings')

app = Celery('Monitoring', broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379")

app.config_from_object('django.conf:settings',  namespace='CELERY')
app.conf.broker_url = "redis://127.0.0.1:6379"
app.conf.result_backend = "redis://127.0.0.1:6379"


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


