import requests

from datetime import datetime
from bs4 import BeautifulSoup

def check():
    try:
        r = requests.get("https://www.alivex.com/order/participantlist/549", timeout=5)
    except requests.exceptions.Timeout:
        print(f"[{datetime.now()}]: The request timed out.")
        return None
    except:
        print(f"[{datetime.now()}]: An unknown error has occurred.")
        return None

    if r.status_code != 200:
        print(f"[{datetime.now()}]: The request returned a status code of {r.status_code}.")
        return None

    bs = BeautifulSoup(r.text, features="html.parser")
    matches = bs.select("tbody > tr")

    if len(matches) == 0:
        print(f"[{datetime.now()}]: Unable to find number of entries.")
        return None

    numEntries = str(len(matches))

    contentFile = "/tmp/skyerciyes-changes"
    try:
        with open(contentFile, "r") as f:
            previousMatch = f.read()
    except:
        previousMatch = ""

    if previousMatch == numEntries:
        print(f"[{datetime.now()}]: All same.")
        return None

    print(f"[{datetime.now()}]: {numEntries} participants.")

    try:
        with open(contentFile, "w") as f:
            f.write(numEntries)
    except:
        print(f"[{datetime.now()}]: The content file could not be written.")
        return None

    return {
        "title": "Skyerciyes",
        "message": f"{numEntries} participants",
    }
