import argparse
import json
import logging
import pytz
import sys

from datetime import datetime
from pytz import timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Read input from command line
parser = argparse.ArgumentParser(description='Send a match notifications message to a channel.')
parser.add_argument('-c', '--credentials', required=True,
        help='Filename of the credentials file to use to send a message')
parser.add_argument('-ch', '--channel', required=True,
        help='Slack channel ID to post the message to')
parser.add_argument('-p', '--people', required=True,
        help='Filename of the club-to-person mappings we care about')

args = parser.parse_args()

# Helper method(s)
def readJSONFile(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

# Credentials loading from local file
'''
{
  "SLACK_BOT_TOKEN": string, # starts with xoxb
  "SLACK_APP_TOKEN": string, # starts with xapp
  "SLACK_SIGNING_SECRET": string
}
'''
credentials_file = args.credentials
SLACK_CREDENTIALS = readJSONFile(credentials_file)
SLACK_BOT_TOKEN = SLACK_CREDENTIALS['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = SLACK_CREDENTIALS['SLACK_APP_TOKEN']
SLACK_SIGNING_SECRET = SLACK_CREDENTIALS['SLACK_SIGNING_SECRET']

# Get the club-to-userId mappings, user ids from Slack users API (see get_channel_users.py script)
'''
club_to_person = {
    'Tottenham': "USER_ID_1",
    'Leeds': "USER_ID_2",
    ...
}

A club being absent in the mapping means we don't care about that club
'''
mapping_file = args.people
club_to_person = readJSONFile(mapping_file)

# Fixture information
''' Fixture object
{
  "home": "Fulham",
  "away": "Arsenal",
  "datetime_utc": "2023-03-11T15:00:00+00:00"
}
'''
all_fixtures = readJSONFile('./fixtures.json')


today = datetime.utcnow().date()

# Compute what fixtures we need to even notify about
fixture_notifications = []
for fixture in all_fixtures:
    # Is this a match up we even care about?
    home_team = fixture['home']
    away_team = fixture['away']
    if home_team in club_to_person and away_team in club_to_person:
        fixture_time = fixture['datetime_utc']
        fixture_datetime = datetime.strptime(fixture_time + " +0000", "%Y-%m-%dT%H:%M:%S %z")
        fixture_date = fixture_datetime.date()

        days_until_game = (fixture_date - today).days
        # Game is tomorrow
        if days_until_game == 1:
            fixture['datetime_utc'] = fixture_datetime
            fixture_notifications.append(fixture)

# Build the notification message
message = "Test notification"
#message = "There are some match ups tomorrow!"
for fixture in fixture_notifications:
    message = message + "\n"

    fixture_datetime = fixture['datetime_utc']
    in_pst = fixture_datetime.astimezone(timezone('US/Pacific'))
    friendly_time = in_pst.strftime("%I%p").lower()

    home = fixture['home']
    away = fixture['away']
    line = "  {} - {} (<@{}>) vs. {} (<@{}>)".format(friendly_time, home, club_to_person[home], away, club_to_person[away])
    message = message + line

# Initializes the web client with your bot token
client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

channel_id = args.channel
try:
    result = client.chat_postMessage(channel=channel_id, text=message)
except SlackApiError as e:
    print(f"Error: {e}")

