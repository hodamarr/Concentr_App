# import os
#
# from django.conf import settings
# from celery import Celery
# # celery cmdline program
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
# app = Celery('app')
# app.config_from_object('django.conf:settings')
#
# app.autodiscover_tasks(settings.INSTALLED_APPS)

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.bin import celery
from redbeat import RedBeatSchedulerEntry

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concentrApp.settings')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'update-throughput-two-min': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'calc_throughput_task',
#         # Schedule
#         'schedule': 60.0,
#     },
# }


def add_task(day, hour, min, participant_code):
    """
    celery.schedules.crontab
    (minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*', **kwargs)
    """
    if day == "-1":
        raise Exception("Invalid day provided")
    interval = celery.schedules.crontab(minute=min, hour=hour, day_of_week=day)  # seconds
    entry = RedBeatSchedulerEntry('send-event', 'tasks.send_event', interval, args=[participant_code])
    entry.save()

def get_day(day):
    weekdays = {
        "monday": "1",
        "tuesday": "2",
        "wednesday": "3",
        "thursday": "4",
        "friday": "5",
        "saturday": "6",
        "sunday": "7"
    }
    return weekdays.get(day.lower(), "-1")