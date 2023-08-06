from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

from concentrApp import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concentrApp.settings')
app = Celery('concentrApp')

# You can add celery settings in settings.py starting with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concentrApp.settings')

app.conf.timezone = "Asia/Jerusalem"


