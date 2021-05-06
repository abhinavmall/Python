import os

import requests
from twilio.rest import Client
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Your Account SID from twilio.com/console
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# Your Auth Token from twilio.com/console
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# Needed to send sms. See Twilio documentation
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM')
ABHINAV_CELL = os.getenv('ABHINAV_NUM')
ASHUTOSH_CELL = os.getenv('ASHUTOSH_NUM')


# Utility class for sending sms via Twilio
class TwilioSms(object):
    def __init__(self):
        self.acc_sid = ACCOUNT_SID
        self.auth_token = AUTH_TOKEN
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, to, text):
        message = self.client.messages.create(
            to=to,
            from_=TWILIO_FROM_NUMBER,
            body=text)
        print('Sent message to' + message.sid)


twilio = TwilioSms()

# Dates to get data for - today and next week (dd-mm-YYYY).
today = datetime.today()
next_week = today + timedelta(days=7)
today_date = today.strftime('%d-%m-%Y')
next_week_date = next_week.strftime('%d-%m-%Y')

# Cowin api for calendar data.
CALENDAR_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
CALENDAR_PARAMS = [{'pincode': "201301", 'date': today_date}, {'pincode': "201301", 'date': next_week_date}]
HEADERS = {'referer': "https://selfregistration.cowin.gov.in/",
           'origin': "https://selfregistration.cowin.gov.in",
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}

# Get a week's data and iterate to find available session for 18-44 category
for CALENDAR_PARAM in CALENDAR_PARAMS:
    print('Checking for ' + str(CALENDAR_PARAM))
    response = requests.get(url=CALENDAR_URL, headers=HEADERS, params=CALENDAR_PARAM)

    # Iterate centers
    for center in response.json()['centers']:
        center_name = center['name']
        center_address = center['address']
        if center['sessions']:
            sessions = center['sessions']
            for session in sessions:
                session_date = session['date']
                session_min_age_limit = session['min_age_limit']
                session_available_capacity = session['available_capacity']
                if (session_available_capacity > 0) and (session_min_age_limit == 18):
                    sms_text = str(
                        session_available_capacity) + ' slots at ' \
                                  + center_name + ', ' \
                                  + center_address + ' on ' + session_date
                    print('SMS Text = ' + sms_text)
                    twilio.send_sms(to=ABHINAV_CELL, text=sms_text)
                    twilio.send_sms(to=ASHUTOSH_CELL, text=sms_text)

print('Completed at ' + str(datetime.now()) + ' for dates = ' + today_date + ' and ' + next_week_date)