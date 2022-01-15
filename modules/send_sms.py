# !!!
# Twilio auth info must be set in environment variables
# !!!

import os
import sys
import aion
from twilio.rest import Client


def send_sms (target, message):
    # sending messages

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=message, from_='+15863316265', to=target)