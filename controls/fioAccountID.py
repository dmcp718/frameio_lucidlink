import requests

def getAccountID(kv_store):
    fToken = kv_store.get("fTokn")


    if fToken is None:
        kv_store.close()
        pass
    else:
        url = "https://api.frame.io/v2/me"

        headers = {"Authorization": "Bearer " + fToken}
        response = requests.get(url, headers=headers)

        data = response.json()
        accountID = data['account_id']
        kv_store.set("frameio_account_id", accountID)
        kv_store.close()
        return accountID
