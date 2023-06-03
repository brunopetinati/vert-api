import json

import requests


def send_push_notification(token, title, message):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "host": "exp.host",
        "Content-Type": "application/json",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
    }
    data = {"to": token, "title": title, "body": message}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.content}")
