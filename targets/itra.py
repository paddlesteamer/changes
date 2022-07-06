import json
import pathlib
import random
import requests

from datetime import datetime
from bs4 import BeautifulSoup

def enabled():
    return True

def check():
    configFilePath = f"{pathlib.Path(__file__).parent.absolute()}/itra.json"

    try:
        with open(configFilePath, "r") as f:
            config = json.load(f)
    except:
        print(f"[{datetime.now()}]: Failed to load config file.")
        return None

    payload = {
        "name" : config["name"],
        "nationality": "",
        "start":"1",
        "count":"10",
        "echoToken": str(random.random())
    }

    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
    }

    try:
        r = requests.post("https://itra.run/api/runner/find", payload, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        print(f"[{datetime.now()}]: The request timed out.")
        return None
    except:
        print(f"[{datetime.now()}]: An unknown error has occurred.")
        return None

    if r.status_code != 200:
        print(f"[{datetime.now()}]: The request returned a status code of {r.status_code}.")
        return None

    data= r.json()

    if data["resultCount"] == 0:
        print(f"[{datetime.now()}]: No runners found.")
        return None

    pi = str(data['results'][0]['pi'])

    contentFile = "/tmp/itra-changes"
    try:
        with open(contentFile, "r") as f:
            previousPi = f.read()
    except:
        previousPi = ""

    if previousPi == pi:
        print(f"[{datetime.now()}]: All same.")
        return None

    print(f"[{datetime.now()}]: New performance index: {pi}")

    try:
        with open(contentFile, "w") as f:
            f.write(pi)
    except:
        print(f"[{datetime.now()}]: The content file could not be written.")
        return None

    return {
        "title": "ITRA",
        "message": f"Performance Index: {pi}",
    }
