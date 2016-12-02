# coding=utf-8

import subprocess
import simplejson as json

from database.config import config


def send_slack_message(message, channel="4space"):
    reply = {}
    reply['text'] = message
    reply['channel'] = "#{channel}".format(channel=channel)
    payload = 'payload={0}'.format(json.dumps(reply))
    subprocess.check_output([
        'curl', '-X', 'POST', '--data-urlencode',
        payload, config["slack_url"]
    ])
