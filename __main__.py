import importlib.machinery
import json
import pathlib
from sys import exc_info
from traceback import print_tb
import requests
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

def runTargets(config: dict):
    try:
        targetsPath = config["modules_path"]
    except:
        targetsPath = f"{pathlib.Path(__file__).parent.absolute()}/targets/"

    for target in pathlib.Path(targetsPath).glob("*.py"):
        module_name = target.name.rstrip('.py')

        try:
            loader = importlib.machinery.SourceFileLoader(module_name, str(target.absolute()))
            m = loader.load_module(module_name)
        except:
            print(f"[{datetime.now()}]: Failed to load module {module_name}.")
            print_tb(exc_info=True)
            continue

        try:
            en = m.enabled()
        except:
            print(f"[{datetime.now()}]: Failed to check if {module_name} is enabled.")
            print_tb(exc_info=True)
            
            # if not implemented yet, assume it is enabled
            en = True

        if not en:
            continue

        res = None
        try:
            res = m.check()
        except:
            print(f"[{datetime.now()}]: Failed to run {module_name}.")
            print_tb(exc_info=True)
            continue

        if res is not None:
            sendNotification(config, res["title"], res["message"])

def main():
    configFilePath = f"{pathlib.Path(__file__).parent.absolute()}/config.json"

    with open(configFilePath, "r") as f:
        config = json.load(f)

    runTargets(config)

if __name__ == '__main__':
    main()
