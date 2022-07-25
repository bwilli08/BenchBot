# Premier League Match Bot

## State of Development
Current implementation as of 2022-07-24:
* Script for scraping Premier League 2022 fixture data from en.as.com and saving to a local `fixtures.json` file
* Script for retrieving the users in a given Slack workspace.
  * Users have to manually map clubs to users, explanation below
* Script for parsing the fixture data, filtering down to "match ups" based on club-to-user data,
filtering further based on matches tomorrow, and then sending a Slack message to a specific Slack channel.
  * Slack channel the message is sent to is also manually configured.

## Running the Scripts

### Fixture Scraping
**Prerequisite: BeautifulSoup must be installed to local Python3 environment.** You can do this with pip: `python3 -m pip install beautifulsoup4`

Script is located at `scrape_data.py` and can be run with `python3 scrape_data.py`. This will save fixtures to a local file named `fixtures.json`.

### Workspace User List
**Prerequisites**
* Slack SDK must be installed to local Python3 environment. You can do this with pip: `python3 -m pip install slack_sdk`
* Premier League Match Bot must be installed to your Slack workspace and have access to the `users:read` scope.
* Slack credentials must be saved to a file with the following format (recommended to be in a `.credentials` folder):
```
{
  "SLACK_BOT_TOKEN": string, # starts with xoxb
  "SLACK_APP_TOKEN": string, # starts with xapp
  "SLACK_SIGNING_SECRET": string
}
```

Script is located at `get_channel_users.py` and can be run with `python3 get_channel_users.py -c PATH_TO_CREDENTIALS_FILE`.
This will return a list of active users in your Slack workspace.
You can then use this list to create a club-to-user file with the following format (recommended to be in a `.users` folder):
```
{
  "CLUB_NAME_FROM_FIXTURES_JSON": "SLACK_USER_ID",
  ...
}
```

The club names should come directly from the `fixtures.json` file, and the Slack User IDs should start with `U` (example: `U0N0QAHJN`).

### Match Up Notifications
**Prerequisites**
* Slack SDK must be installed to local Python3 environment. You can do this with pip: `python3 -m pip install slack_sdk`
* Premier League Match Bot must be installed to your Slack workspace and have access to the `channels:read` and `chat:write` scopes.
* Slack credentials must be saved to a file with the following format (recommended to be in a `.credentials` folder):
```
{
  "SLACK_BOT_TOKEN": string, # starts with xoxb
  "SLACK_APP_TOKEN": string, # starts with xapp
  "SLACK_SIGNING_SECRET": string
}
```
* The above scripts above should be run and you should have a list of fixtures and a mapping of clubs to Slack user ids.
* The Slack app should be added to a specific channel in your workspace. The ID of this channel should then be retrieved with the [connections_list API](https://api.slack.com/methods/conversations.list)

Script is located at `notify_slack.py` and can be run with `python3 notify_slack.py -c PATH_TO_CREDENTIALS_FILE -ch CHANNEL_ID -p PATH_TO_CLUB_TO_USERS_FILE`.
If there are "match ups" tomorrow, this will send a Slack message to the given channel listing all of the match ups, as well as tagging the given users. Example:
```
There are some match ups tomorrow!
  07am - Leeds (@Person) vs. Wolves (@OtherPerson)
  07am - Tottenham (@AnotherPerson) vs. Southampton (@MorePeople)



