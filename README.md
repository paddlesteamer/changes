# ping-tbt
This is a forked version of [ping-sm](https://github.com/utkuufuk/ping-sm). Run this script periodically as a cron job. It will check if there is a new call in [TUBITAK Funds](https://tubitak.gov.tr/tr/destekler/sanayi/ulusal-destek-programlari). 

## How it works
 * Sends you a warning if there is a change in calls.

#### Notifications
You need a [Mailgun domain](https://documentation.mailgun.com/en/latest/api-domains.html) or a [Telegram bot](https://core.telegram.org/bots) in order to enable notifications. You'll have to rely on logs otherwise.

## Installing dependencies
```sh
pip3 install -r requirements.txt
```

## Configuraiton
 1. Copy `.env.example` and name the new file as `.env`
 2. Set each variable in `.env` with your own values. 

## Launching
```sh
# launch manually
python3 ping-tbt

# launch manually with notification emails enabled
python3 ping-tbt --email

# launch manually with telegram messages enabled
python3 ping-tbt --telegram

# example cron job
0 10 * * * /usr/bin/python3 /path-to-ping-tbt/ping-tbt --email 2>&1 >> /path-to-your-log-file/log.log
```
