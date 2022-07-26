#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import json
import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Read input from command line
parser = argparse.ArgumentParser(description='Output the users in a channel')
parser.add_argument('-c', '--credentials', required=True,
        help='Filename of the credentials file containing Slack credentials')

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

# Initializes the web client with your bot token
client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

try:
    users_list = client.users_list()
    for member in users_list['members']:
        if not member['deleted']:
            print((member['id'], member['name'], member['profile']['display_name']))
except SlackApiError as e:
    print(f"Error: {e}")

