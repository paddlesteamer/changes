# changes
Track changes to web sites and notify via home assistant notify service if there is any.

## Installing dependencies
```sh
pip3 install -r requirements.txt
```

## Configuraiton
 1. Copy `config.json.example` and name the new file as `config.json`
 2. Set each variable in `config.json` with your own values. 

## Launching
```sh
# launch manually
python3 changes

# example cron job
0 10 * * * /usr/bin/python3 /path-to-changes 2>&1 >> /path-to-your-log-file/log.log
```