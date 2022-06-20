# changes
Track changes to web sites (or anything you wish) and notify via home assistant notify service if there is any.

## Installing dependencies
```sh
pip3 install -r requirements.txt
```

## Configuraiton
 - Copy `config.json.example` and name the new file as `config.json`
 - `config.json` needs three variables which are `ha_url`, `ha_token` and `ha_device`.
 - `ha_url` is the URL of your home assistant instance. If `changes` will run on the same machine with home assistant, it probably would be `http://127.0.0.1:8123`.
 - `ha_token` is long-lived access token for home assistant. You can create yours from home assistant dashboard. Go to your profile, at the bottom of the page you'll see `Long-Lived Access Tokens`. Click `Create Token`.
 - `ha_device` is the name of the notify service that`changes` will call. You can find it from `Developer Tools->Services`. It would be something like `mobile_app_xxx`.

 ## How to use
You need to write a python code which implements `check()` method and place it into `targets` directory. `changes` will call `check()` method of each file automatically every time it runs.

Your implementation of `check()` should return a json that has `title` and `message` fields. These are the title and message part of your notification. If you don't want `changes()` to send notification (i.e. there is no change on the web site), you should return `None`. See example implementations.

## Launching
```sh
# launch manually
python3 changes

# example cron job that runs every 5 min
*/5 * * * * /usr/bin/python3 /path-to-changes 2>&1 >> /path-to-your-log-file/log.log
```