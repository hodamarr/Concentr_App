
from redbeat import RedBeatSchedulerEntry
from concentrApp.tasks import notify

from application.models import Schedule
from celery.schedules import crontab
from celery.schedules import crontab
import celery
def create_celery_beat_schedule(task):
    hour, minute = task.ping_times.split(':')
    expo_token = task.participant.expo_token
    interval = celery.schedules.crontab(minute=minute, hour=hour, day_of_week="0-6")  # seconds
    entry = RedBeatSchedulerEntry(str(task.id), 'concentrApp.tasks.notify', interval, args=[expo_token,
                                                                                             task.context.id], app=app)
    entry.save()


def update_celery_beat_schedule(task):
    delete_celery_beat_schedule(task)
    create_celery_beat_schedule(task)


def delete_celery_beat_schedule(task):
    key = "redbeat:" + str(task.id)
    entry = RedBeatSchedulerEntry.from_key(key, app=app)
    entry.delete()

