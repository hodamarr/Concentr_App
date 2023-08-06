from datetime import datetime
import celery
from celery import shared_task
from redbeat import RedBeatSchedulerEntry

from application.models import Schedule
from concentrApp.celery import app
from celery.schedules import crontab
from notify_task import send_message


def create_celery_beat_schedule(task):
    hour, minute = task.ping_times.split(':')
    expo_token = task.participant.expo_token
    interval = celery.schedules.crontab(minute=int(minute), hour=int(hour), day_of_week="0-6")  # seconds
    entry = RedBeatSchedulerEntry(str(task.id), 'concentrapp.tasks.notify', interval, args=[expo_token,
                                                                                             task.context.id], app=app,)
    entry.save()


def update_celery_beat_schedule(task):
    _id = task.id
    entry = RedBeatSchedulerEntry(str(_id), app=app)
    a = 5

@shared_task
def notify(participant_token, context):
    body = {"context": context}
    print("send message with " + participant_token + " context: " + str(context))
    send_message(participant_token, "QUIZ", body)



