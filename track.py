import argparse
import json
import requests
from datetime import datetime
from requests_hawk import HawkAuth


USER_ID = ''
API_KEY = ''
TIMEZONE_NAME = 'CEST'
TIMEZONE = '+0100'


def get_time():
    (dt, micro) = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')

    return '%s.%03dZ' % (dt, int(micro) / 1000)


def do_start():
    payload = {
        'userId': USER_ID,
        'start': get_time(),
        'end': None,
        'timezoneName': TIMEZONE_NAME,
        'timezone': TIMEZONE,
        'type': 'work'
    }

    url = 'https://app.absence.io/api/v2/timespans/create'
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=USER_ID, key=API_KEY, server_url=url)

    request_response = requests.post(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})

    return request_response

def pause_start():
    stop_response = do_stop()
    if stop_response is not False and stop_response.ok:
        print('Worktime stop Done.')
    else:
        print('Error: ' + stop_response.text)
    payload = {
        'userId': USER_ID,
        'start': get_time(),
        'end': None,
        'timezoneName': TIMEZONE_NAME,
        'timezone': TIMEZONE,
        'type': 'break'
    }

    url = 'https://app.absence.io/api/v2/timespans/create'
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=USER_ID, key=API_KEY, server_url=url)

    request_response = requests.post(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})

    return request_response

def pause_stop():
    stop_response = do_stop()
    if stop_response is not False and stop_response.ok:
        print('Breaktime stop Done.')
    else:
        print('Error: ' + stop_response.text)
    start_response = do_start()
    return start_response

def do_stop():
    payload = {
        'filter': {
            'userId': USER_ID,
            'end': {'$eq': None}
        },
        'limit': 10,
        'skip': 0
    }

    url = 'https://app.absence.io/api/v2/timespans'
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=USER_ID, key=API_KEY, server_url=url)

    request_response = requests.post(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})
    if request_response.ok:
        request_response = json.loads(request_response.text)
        entry = request_response['data'][0]
    else:
        return False

    payload = {
        'start': entry['start'],
        'end': get_time(),
        'timezoneName': TIMEZONE_NAME,
        'timezone': TIMEZONE
    }

    url = 'https://app.absence.io/api/v2/timespans/{}'.format(entry['_id'])
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=USER_ID, key=API_KEY, server_url=url)

    request_response = requests.put(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})

    return request_response

parser = argparse.ArgumentParser()
parser.add_argument('do', help='start/stop')
args = parser.parse_args()

if args.do == 'start':
    response = do_start()
elif args.do == 'pause-start':
    response = pause_start()
elif args.do == 'pause-stop':
    response = pause_stop()
else:
    response = do_stop()

if response is not False and response.ok:
    print('Done.')
else:
    print('Error: ' + response.text)
