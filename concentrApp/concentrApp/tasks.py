from datetime import datetime
import celery
from celery import shared_task
from redbeat import RedBeatSchedulerEntry

from application.models import Schedule
from concentrApp.celery import app
from celery.schedules import crontab

app.conf.beat_schedule = {
    'my_sch': {
        "task": "concentrApp.tasks.notify",  # Replace with the actual task path
        "schedule": crontab(38, 21, day_of_week="0-6"),
        "args": ("abc", "efd",),  # Additional arguments if needed
    }
}

def update_celery_beat_schedule():
    tasks = Schedule.objects.all()
    new_schedule = {}

    for task in tasks:
        hour, minute = task.ping_times.split(':')
        expo_token = task.participant.expo_token
        # new_schedule[str(task.id)] = {
        #     "task": "myapp.tasks.notify",  # Replace with the actual task path
        #     "schedule": crontab(minute=int(minute), hour=int(hour), day_of_week="0-6"),
        #     "args": (expo_token, task.context.id),  # Additional arguments if needed
        # }
        interval = celery.schedules.crontab(minute=int(minute), hour=int(hour), day_of_week="0-6")  # seconds
        entry = RedBeatSchedulerEntry(str(task.id), 'concentrapp.tasks.notify', interval, args=[expo_token,
                                                                                                task.context.id],
                                      app=app,)
        entry.save()

    print(app.conf.beat_schedule)


@shared_task
def notify(participant_token, context):
    with open('output.txt', 'a') as file:
        file.write(context + participant_token + '\n')

