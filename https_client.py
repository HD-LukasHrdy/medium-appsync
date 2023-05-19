# subscription_client.py


####################################################################################################################
######     https://aws.amazon.com/blogs/mobile/appsync-websockets-python     #######################################
####################################################################################################################

from base64 import b64encode, decode
from datetime import datetime
from uuid import uuid4

import websocket
import threading

import json

# Constants Copied from AppSync API 'Settings'
API_URL = "https://rwtvzb7lyzabvmrds6pdtn3bsi.appsync-api.eu-central-1.amazonaws.com"
API_KEY = "da2-yv6envsjvnbjhexps2sbouc7je"

# GraphQL's subscription Registration object
GQL_SUBSCRIPTION = json.dumps({
    'query': 'subscription OnAddTenant { somethingChanged{ userId companyId } }',
    'variables': {}
})

# Discovered values from the AppSync endpoint (API_URL)
WSS_URL = API_URL.replace('https', 'wss').replace('appsync-api', 'appsync-realtime-api')
HOST = API_URL.replace('https://', '').replace('/graphql', '')

# Subscription ID (client generated)
SUB_ID = str(uuid4())

# Set up Timeout Globals
timeout_timer = None
timeout_interval = 10
amount_of_messages = 0


# Calculate UTC time in ISO format (AWS Friendly): YYYY-MM-DDTHH:mm:ssZ
def header_time():
    return datetime.utcnow().isoformat(sep='T', timespec='seconds') + 'Z'


# Encode Using Base 64
def header_encode(header_obj):
    return b64encode(json.dumps(header_obj).encode('utf-8')).decode('utf-8')


# reset the keep alive timeout daemon thread
def reset_timer(ws):
    global timeout_timer
    global timeout_interval

    if (timeout_timer):
        timeout_timer.cancel()
    timeout_timer = threading.Timer(timeout_interval, lambda: ws.close())
    timeout_timer.daemon = True
    timeout_timer.start()


# Create API key authentication header
api_header = {
    'host': HOST,
    'x-api-key': API_KEY
}


if __name__ == '__main__':

