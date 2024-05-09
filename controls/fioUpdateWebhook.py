import requests

def updateWebhook(kv_store, webhook_id, webhook_name, whurl):
    fToken = kv_store.get("fTokn")

    # Check if fToken is None or empty
    if not fToken:
        print("Frame.io token is not available. Skipping update.")
        return False

    # Check if id is None or empty
    if not webhook_id:
        print("Webhook ID is not available. Skipping update.")
        return False

    # Check if the webhook URL is None or empty
    if not whurl:
        print("Webhook URL is not available. Skipping update.")
        return False
    
    hook_id = webhook_id
    url = "https://api.frame.io/v2/hooks/" + hook_id

    payload = {
        "name": webhook_name,
        "url": whurl
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + fToken
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        data = response.json()

        if 'error' in data:
            print(f"Error updating webhook: {data['error']}")
            return False
        else:
            return True

    except Exception as e:
        print(f"Error updating webhook: {str(e)}")
        return False