import requests

def getAccountName(kv_store):
    fToken = kv_store.get("fTokn")
    
    if fToken is None:
        kv_store.close()
        return None
    else:
        url = "https://api.frame.io/v2/me"

        headers = {"Authorization": "Bearer " + fToken}
        response = requests.get(url, headers=headers)

        data = response.json()
        accountName = data['name']
        kv_store.set("frameio_account_name", accountName)
        kv_store.close()
        return accountName
