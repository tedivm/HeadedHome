import datetime
import os
from pytz import timezone
import requests

from twilio.rest import Client

twilio_client = Client(os.environ['TWILIO_ACCOUNT'], os.environ['TWILIO_TOKEN'])

START_STATION = 'DBRK'
DIRECTION = 'WARM'

BART_TIME = 34
BART_WALK = 6
BART_WALK_VARIANCE = 0.5
HOME_WALK = 15
TRAVEL_BUFFER = 10

BART_API_KEY = os.environ.get('BART_API_KEY', 'MW9S-E7SL-26DU-VV8V')


def get_question_message():
    trains = get_next_trains()
    arrival = get_home_estimate()
    message = 'The next catchable trains arrive in %s and %s minutes, leaving you to get home between %s and %s.'
    return message % (trains[0], trains[1], arrival[0], arrival[1])

def get_so_notification_message():
    arrival = get_home_estimate()
    message = 'Robert has left the office and will arrive between %s and %s.'
    return message % (arrival[0], arrival[1])

def send_message(message, number):
    print('sending message from sms')
    sms = twilio_client.messages.create(
        body=message,
        to=number,    # Replace with your phone number
        from_=os.environ['TWILIO_PHONE'])  # Replace with your Twilio number
    print(sms.sid)

def get_home_estimate():
    trains = get_next_trains()
    transit_time = BART_TIME + HOME_WALK
    now = datetime.datetime.now(timezone('America/Los_Angeles'))
    window_start = now + datetime.timedelta(minutes = (trains[0] + transit_time))
    if trains[0] >= BART_WALK + (BART_WALK * BART_WALK_VARIANCE):
        window_end = now + datetime.timedelta(minutes = (trains[0] + transit_time + TRAVEL_BUFFER))
    else:
        window_end = now + datetime.timedelta(minutes = (trains[1] + transit_time + TRAVEL_BUFFER))
    return [window_start.strftime('%-I:%M'), window_end.strftime('%-I:%M')]

def get_next_trains():
    payload = {
        'cmd': 'etd',
        'key': BART_API_KEY,
        'orig': START_STATION,
        'json': 'y'
    }
    r = requests.get(url='http://api.bart.gov/api/etd.aspx', params=payload)
    r.raise_for_status()
    results = r.json()

    times = []
    for destination in results['root']['station'][0]['etd']:
        if destination['abbreviation'] != DIRECTION:
            continue
        for estimates in destination['estimate']:
            time = int(estimates['minutes'])
            if time > BART_WALK:
                times.append(time)
    return times


class Actions():

    def request_times(self):
        send_message(get_question_message(), os.environ['MY_NUMBER'])

    def going_home(self):
        send_message(get_question_message(), os.environ['MY_NUMBER'])
        send_message(get_so_notification_message(), os.environ['SO_NUMBER'])

    def test_messages(self):
        print(get_question_message())
        print(get_so_notification_message())

    def __repr__(self):
        return ''


def lambda_handler(event, context):
    print(event)
    print(context)
    print(event['clickType'])

    actions = Actions()
    if event['clickType'] == 'SINGLE':
        actions.request_times()
    if event['clickType'] == 'DOUBLE':
        actions.going_home()
    if event['clickType'] == 'LONG':
        pass

def fire_handler():
    import fire
    fire.Fire(Actions)


if __name__ == "__main__":
    fire_handler()
