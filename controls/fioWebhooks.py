import os
import requests
import json
from .KeyValueStore import KeyValueStore

def create_dict_from_json(kv_store, url, path, headers):
    webhooksKV = {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for i in data:
            webhooksKV[i['name']] = i['id']
        # Write the result dictionary to a file
        with open(path, 'w') as file:
            file.write(json.dumps(webhooksKV))
    else:
        print("Failed to retrieve JSON data from", url)

def getWebhooks(kv_store, account_id):
    userPath = os.path.expanduser('~')
    wh_path = userPath + "/.lucidlinkFrameIOapp/webhooks.json"
    kv_store = KeyValueStore()
    fToken = kv_store.get("fTokn")
    kv_store.close()

    if fToken is None:
        return
    else:
        account_id = account_id
        url = "https://api.frame.io/v2/accounts/" + account_id + "/hooks"

        headers = {"Authorization": "Bearer " + fToken}

        create_dict_from_json(kv_store, url, wh_path, headers=headers)

        response = requests.get(url, headers=headers)

        webhooks = []
        data = response.json()
        for i in data:
            webhooks.append(i['name'])

        return webhooks