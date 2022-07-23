#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from datetime import datetime
import json
import time
import requests

# Idea of the Slack Bot:
# Step One: Find all of the fixtures and times. Save these somewhere (locally/S3)
#           Fixture object is just {home, away, utc_time}
# Step Two: Create a local mapping of {team name -> person} i.e. Liverpool: Brent
# Step Three: Set up Slack bot/notification
# Step Four: Once a day, loop over the fixtures again to verify accuracy.
# Step Five: Once a day, look at the fixture list and notify the slack bot of matchups happening tomorrow
# Example message:
#   Tomorrow's matchups!
#    - 7 a.m. : Wolverhampton Wanderers (@Cameron) vs. AFC. Bournemouth (@Brandan)

club_to_person = {
        'Tottenham': "@nateee",
        'Leeds': "@cbotcritter",
        'Wolves': "@ckoizumil",
        'Bournemouth': "@brandan",
        'M. United': "@al",
        'Southampton': "@jonnyrottin",
        'Newcastle': "Marcus",
        'Crystal Palace': "@Zach",
        'Nottingham Forest': "@kwong",
        'Liverpool': "@thealpacca"
}

''' Fixture object
{
  "home": "Fulham",
  "away": "Arsenal",
  "datetime_utc": "2023-03-11T15:00:00+00:00"
}
'''
fixture_filename = "./fixtures.json"
with open(fixture_filename, 'r') as fixture_file:
    all_fixtures = json.loads(fixture_file.read())


#today = datetime.utcnow().date()
today = datetime.strptime("2022-08-05T10:00:00", "%Y-%m-%dT%H:%M:%S").date()

games_to_notify = []
for fixture in all_fixtures:
    # Is this a match up we even care about?
    home_team = fixture['home']
    away_team = fixture['away']
    if home_team in club_to_person and away_team in club_to_person:
        print("This is a match up! {} vs {}".format(club_to_person[home_team], club_to_person[away_team]))

        fixture_time = fixture['datetime_utc']
        fixture_date = datetime.strptime(fixture_time, "%Y-%m-%dT%H:%M:%S").date()

        days_until_game = (fixture_date - today).days

        # Game is tomorrow
        if days_until_game == 1:
            print("Game is tomorrow, game should be included in Slack Bot message")



