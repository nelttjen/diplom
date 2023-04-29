import os
from celery import Celery
from diplom.settings import INSTALLED_APPS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')

celery_app = Celery('diplom')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: INSTALLED_APPS)