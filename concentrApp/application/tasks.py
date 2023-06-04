from __future__ import absolute_import, unicode_literals
from celery import shared_task
# import datetime
#
#
# @app.task(name="send-event")
# def send_event(participant_code):
#     # Get the current date and time
#     current_datetime = datetime.datetime.now()
#
#     # Format the date and time as a string
#     formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#
#     # Construct the string to be written
#     content = "beat " + formatted_datetime + "\n"
#
#     # Open the file in append mode
#     with open("output.txt", "a") as file:
#         # Write the content to the file
#         file.write(content)