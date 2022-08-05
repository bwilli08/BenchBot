#!/bin/sh

# We want to run at 5pm PST -> 12am UTC
echo "0 0 * * * ubuntu /bin/python3 /home/ubuntu/PremierLeagueMatchBot/scripts/scrape_data.py -f /home/ubuntu/PremierLeagueMatchBot/data/fixtures.json &> /home/ubuntu/PremierLeagueMatchBot/fixtures-\$(date +%s).log" > /etc/cron.d/update_fixtures
echo "0 0 * * * ubuntu /bin/python3 /home/ubuntu/PremierLeagueMatchBot/scripts/notify_slack.py -c .credentials/cavilist_channel_credentials -ch C0MKGPY1K -p .users/cavilist.json -f /home/ubuntu/PremierLeagueMatchBot/data/fixtures.json &> /home/ubuntu/PremierLeagueMatchBot/notify-\$(date +%s).log" > /etc/cron.d/notify_slack
