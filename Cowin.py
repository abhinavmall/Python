import os

import requests
from twilio.rest import Client
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

# Your Account SID from twilio.com/console
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
# Your Auth Token from twilio.com/console
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

twilio_from = os.getenv('TWILIO_FROM')
abhinav_num = os.getenv('ABHINAV_NUM')
ashutosh_num = os.getenv('ASHUTOSH_NUM')


# Send Message
class TWILIO_SMS(object):
    def __init__(self):
        self.acc_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def sendSms(self, to, text):
        message = self.client.messages.create(
            to=to,
            from_=twilio_from,
            body=text)
        print('Sent message to' + message.sid)


twilio_sms = TWILIO_SMS()

today = datetime.today()
next_week = today + timedelta(days=7)
today_date = today.strftime('%d-%m-%Y')
next_week_date = next_week.strftime('%d-%m-%Y')

# Get calendar data
CALENDAR_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
CALENDAR_PARAMS = [{'pincode': "201301", 'date': today_date}, {'pincode': "201301", 'date': next_week_date}]

for CALENDAR_PARAM in CALENDAR_PARAMS:
    response = requests.get(url=CALENDAR_URL, params=CALENDAR_PARAM)
    print('Checking for ' + str(CALENDAR_PARAM))
    # Get centers list
    centers = response.json()['centers']

    for center in centers:
        center_name = center['name']
        center_address = center['address']
        if center['sessions']:
            sessions = center['sessions']
            for session in sessions:
                session_date = session['date']
                session_min_age_limit = session['min_age_limit']
                session_available_capacity = session['available_capacity']
                if (session_available_capacity > 0) and (session_min_age_limit == 18):
                    message = str(
                        session_available_capacity) + ' slots at ' + center_name + ', ' + center_address + ' on ' + session_date
                    twilio_sms.sendSms(to=abhinav_num, text=message)
                    twilio_sms.sendSms(to=ashutosh_num, text=message)
                    print(message)

print('Completed at ' + str(datetime.now()) + ' for dates = ' + today_date + ' and ' + next_week_date)
