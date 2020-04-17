import os
import sys
import requests
import argparse
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from datetime import datetime
from dotenv import load_dotenv


# a lock file will ensure that we won't spam ourselves with notifications
def writeLockFile():
    with open(os.getenv("LOCK_FILE"), "w") as f:
        f.write("")


def sendEmail(subject, message):
    try:
        requests.post(
            os.getenv('MAILGUN_DOMAIN'),
            auth=("api", os.getenv('MAILGUN_SECRET')),
            data={
                "from": os.getenv('EMAIL_FROM'),
                "to": [os.getenv('EMAIL_TO')],
                "subject": subject,
                "text": message
            }
        )
        writeLockFile()
    except:
        print(f"[{datetime.now()}]: Could not send email with subject: '{subject}'")


def sendTelegramMessage(message):
    try:
        token = os.getenv("TELEGRAM_TOKEN")
        r = requests.get(
            f"https://api.telegram.org/bot{token}/sendMessage",
            params={
                "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                "text": message,
            })
        if r.status_code == 200 and r.json()["ok"]:
            writeLockFile()
            return
        raise Exception
    except:
        print(f"[{datetime.now()}]: Could not send telegram message.")


def main():
    # read program arguments and environment variables
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', type=bool, nargs='?', const=True, default=False,
                        help='Enable notification emails')
    parser.add_argument('-t', '--telegram', type=bool, nargs='?', const=True, default=False,
                        help='Enable Telegram notification messages')
    parser.add_argument('-v', '--verbose', type=bool, nargs='?', const=True, default=False,
                        help='Verbose output')
    args = parser.parse_args()

    try:
        r = requests.get(os.getenv('URL'), timeout=5)
    except Timeout:
        print(f"[{datetime.now()}]: The request timed out.")
        sys.exit(1)

    bs = BeautifulSoup(r.text, features="html.parser")
    div = bs.find(id="block-views-acik-cagrilar-view-block")
    if div is None:
        content = ""
    else:
        content = div.text.strip("\n")

    try:
        with open(os.getenv('CONTENT_FILE'), "r") as f:
            previousContent = f.read()
    except:
        previousContent = ""

    if previousContent == content:
        print(f"[{datetime.now()}]: All same.")
        if args.verbose:
            print(f"{content}")
        sys.exit(0)

    message = f"[{datetime.now()}]: There is a change: {os.getenv('URL')}\n"
    message += f"{content}"
    print(message)

    if args.email:
        sendEmail("Change!", message)
    if args.telegram:
        sendTelegramMessage(message)

    try:
        with open(os.getenv('CONTENT_FILE'), "w") as f:
            f.write(content)
    except:
        print(f"[{datetime.now()}]: The content file could not be written.")
        sys.exit(1)

if __name__ == '__main__':
    main()
