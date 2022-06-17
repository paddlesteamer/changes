import json
import pathlib
import requests
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from datetime import datetime

def sendNotification(config: dict, title: str, message: str):
    haRestURL = f"{config['ha_url']}/api/services/notify/{config['ha_device']}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['ha_token']}",
    }

    payload = {
        "title": title,
        "message": message,
    }

    try:
        r = requests.post(haRestURL, headers=headers, json=payload, timeout=15)
    except Timeout:
        print(f"[{datetime.now()}]: Home assistant request timed out.")
        return
    except:
        print(f"[{datetime.now()}]: Home assistant request failed.")


def check(config: dict):
    try:
        r = requests.get("https://www.alivex.com/order/participantlist/549", timeout=5)
    except Timeout:
        print(f"[{datetime.now()}]: The request timed out.")
        return
    except:
        print(f"[{datetime.now()}]: An unknown error has occurred.")
        return

    if r.status_code != 200:
        print(f"[{datetime.now()}]: The request returned a status code of {r.status_code}.")
        return

    bs = BeautifulSoup(r.text, features="html.parser")
    matches = bs.select("tbody > tr")

    if len(matches) == 0:
        print(f"[{datetime.now()}]: Unable to find number of entries.")
        return

    numEntries = str(len(matches))

    try:
        with open(config["content_file"], "r") as f:
            previousMatch = f.read()
    except:
        previousMatch = ""

    if previousMatch == numEntries:
        print(f"[{datetime.now()}]: All same.")
        return

    # not first call
    if previousMatch != "":
        sendNotification(config, "Skyerciyes", f"{numEntries} participants.")

    print(f"[{datetime.now()}]: {numEntries} participants.")

    try:
        with open(config["content_file"], "w") as f:
            f.write(numEntries)
    except:
        print(f"[{datetime.now()}]: The content file could not be written.")
        return


def main():
    configFilePath = f"{pathlib.Path(__file__).parent}/config.json"

    with open(configFilePath, "r") as f:
        config = json.load(f)

    check(config)

if __name__ == '__main__':
    main()
