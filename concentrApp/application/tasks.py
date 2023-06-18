from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime


@shared_task(name="mytask")
def task(participant_token):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    with open('output.txt', 'a') as file:
        file.write(formatted_datetime + participant_token + '\n')
