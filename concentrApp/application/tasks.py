from celery import shared_task

@shared_task(name="send-event")
def send_event(participant_code):
    print("Sending event to", participant_code)