#!/bin/sh

# We want to run at 5pm PST on Thursdays -> 12am UTC on Fridays
echo "0 0 * * fri ubuntu /bin/python3 /home/ubuntu/PremierLeagueMatchBot/scripts/scrape_data.py -f /home/ubuntu/PremierLeagueMatchBot/data/fixtures.json &> /home/ubuntu/PremierLeagueMatchBot/fixtures-\$(date +%s).log" > /etc/cron.d/update_fixtures
echo "0 0 * * fri ubuntu /bin/python3 /home/ubuntu/PremierLeagueMatchBot/scripts/notify_slack.py -c /home/ubuntu/PremierLeagueMatchBot/.credentials/cavilist_channel_credentials -ch C0MKGPY1K -p /home/ubuntu/PremierLeagueMatchBot/.users/cavilist.json -f /home/ubuntu/PremierLeagueMatchBot/data/fixtures.json &> /home/ubuntu/PremierLeagueMatchBot/notify-\$(date +%s).log" > /etc/cron.d/notify_slack
