from celery import shared_task
from notify_task import send_message

@shared_task
def notify(participant_token, context):
    body = {"context": context}
    if participant_token == None or context == None:
        print("context or token is None")
    else:
        print("send message with " + participant_token + " context: " + str(context))
        send_message(participant_token, "QUIZ", body)



