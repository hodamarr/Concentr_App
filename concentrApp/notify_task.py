import requests as req


def send_message(expo_token, title, body):
    message = {
        'to': expo_token,
        'title': title,
        'body': body
    }
    return req.post('https://exp.host/--/api/v2/push/send', json=message)
