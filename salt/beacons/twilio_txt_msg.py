# -*- coding: utf-8 -*-
'''
Beacon to emit Twilio text messages
'''

# Import Python libs
from __future__ import absolute_import
from datetime import datetime
import logging

# Import 3rd Party libs
try:
    from twilio.rest import TwilioRestClient
    HAS_TWILIO = True
except ImportError:
    HAS_TWILIO = False

log = logging.getLogger(__name__)

__virtualname__ = 'twilio_txt_msg'


def __virtual__():
    if HAS_TWILIO:
        return __virtualname__
    else:
        return False


def beacon(config):
    '''
    Emit a dict name "texts" whose value is a list
    of texts.

    .. code-block:: yaml

        beacons:
          twilio_txt_msg:
            account_sid: "<account sid>"
            auth_token: "<auth token>"
            twilio_number: "+15555555555"
            poll_interval: 10

    poll_interval defaults to 10 seconds
    '''
    log.trace('twilio_txt_msg beacon starting')
    ret = []
    if not all([config['account_sid'], config['auth_token'], config['twilio_number']]):
        return ret
    output = {}
    poll_interval = config.get('poll_interval')
    if not poll_interval:
        # Let's default to polling every 10 secons
        poll_interval = 10
    now = datetime.now()
    if 'twilio_txt_msg' in __context__:
        timedelta = now - __context__['twilio_txt_msg']
        if timedelta.seconds < poll_interval:
            log.trace('Twilio beacon poll interval not met.')
            log.trace('Twilio polling in {0}'.format(poll_interval - timedelta.seconds))
            return ret

    output['texts'] = []
    client = TwilioRestClient(config['account_sid'], config['auth_token'])
    messages = client.messages.list(to=config['twilio_number'])
    log.trace('Num messages: {0}'.format(len(messages)))
    if len(messages) < 1:
        log.trace('Twilio beacon has no texts')
        __context__['twilio_txt_msg'] = now
        return ret

    for message in messages:
        item = {}
        item['id'] = str(message.sid)
        item['body'] = str(message.body)
        item['from'] = str(message.from_)
        item['sent'] = str(message.date_sent)
        item['images'] = []

        if int(message.num_media):
            media = client.media(message.sid).list()
            if len(media):
                for pic in media:
                    item['images'].append(str(pic.uri))
        output['texts'].append(item)
        message.delete()
    __context__['twilio_txt_msg'] = now
    ret.append(output)
    return ret
