from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.bin import celery
from redbeat import RedBeatSchedulerEntry

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concentrApp.settings')

app = Celery('concentrapp_concentrApp')
app.conf.broker_url = 'redis://localhost:6379/0'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import datetime


@app.task(name="send-event")
def send_event(participant_code):
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Construct the string to be written
    content = "beat " + formatted_datetime + "\n"

    # Open the file in append mode
    with open("output.txt", "a") as file:
        # Write the content to the file
        file.write(content)

# app.conf.beat_schedule = {
#     'update-throughput-two-min': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'calc_throughput_task',
#         # Schedule
#         'schedule': 60.0,
#     },
# }


def add_task(day, hour, min, participant_code, context):
    """
    celery.schedules.crontab
    (minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*', **kwargs)
    """
    if day == "-1":
        raise Exception("Invalid day provided")
    interval = celery.schedules.crontab(minute=min, hour=hour, day_of_week=day)  # seconds
    entry = RedBeatSchedulerEntry('send-event', 'tasks.send_event', interval, args=[participant_code, context])
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