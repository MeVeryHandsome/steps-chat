import json

import requests

def call_with_messages(prompt):
    url = "http://123.57.244.236:15103/xchat-answer/v1/api/chat"
    payload = {
        "question": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return content['data']
    else:
        print("Failed to get response, status code:", response.status_code)

def call_with_stream(prompt):
    url = "http://123.57.244.236:15103/xchat-answer/v1/api/eventchat"
    payload = {
        "question": prompt
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8')[len("data: "):])["data"]
                yield decoded_line
    else:
        print("Failed to get response, status code:", response.status_code)