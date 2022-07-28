#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import json
import requests
import time
from bs4 import BeautifulSoup

# Idea of this script and the Slack Bot:
# Step One: Find all of the fixtures and times. Save these somewhere (locally/S3)
#           Fixture object is just {home, away, utc_time}
# Step Two: Create a local mapping of {team name -> person} i.e. Liverpool: Brent
# Step Three: Set up Slack bot/notification
# Step Four: Once a day, loop over the fixtures again to verify accuracy.
# Step Five: Once a day, look at the fixture list and notify the slack bot of matchups happening tomorrow
# Example message:
#   Tomorrow's matchups!
#    - 7 a.m. : Wolverhampton Wanderers (@Cameron) vs. AFC. Bournemouth (@Brandan)

# Example "fixture" HTML
'''
<li class="list-resultado">
    <div class="equipo-local" itemprop="performer" itemscope="" itemtype="http://schema.org/SportsTeam">
        <a class="cont-enlace-equipo" href="/resultados/ficha/equipo/west_ham/73/" itemprop="url" title="West Ham: Show more info">
            <span class="nombre-equipo" itemprop="name">West Ham</span>
            <span class="cont-img-escudo">
                <img alt="Badge/Flag West Ham" data-src="https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/73.png" data-srcset="https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/73.png 1x, https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/73.png 2x" itemprop="image" onerror="this.src='//as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/sin_logo.png';this.srcset='//as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/sin_logo.png';return;" onload="lzld(this)" src="//as01.epimg.net/t.gif" srcset="//as01.epimg.net/t.gif 200w"/>
            </span>
        </a>
    </div>
    <div class="cont-resultado no-comenzado">
        <span class="resultado">Su 11:30</span>
    </div>
    <div class="equipo-visitante" itemprop="performer" itemscope="" itemtype="http://schema.org/SportsTeam">
        <a class="cont-enlace-equipo" href="/resultados/ficha/equipo/m_city/66/" itemprop="url" title="M. City: Show more info">
            <span class="cont-img-escudo">
                <img alt="Badge/Flag M. City" data-src="https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/66.png" data-srcset="https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/66.png 1x, https://as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/66.png 2x" itemprop="image" onerror="this.src='//as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/sin_logo.png';this.srcset='//as01.epimg.net/img/comunes/fotos/fichas/equipos/x-small/sin_logo.png';return;" onload="lzld(this)" src="//as01.epimg.net/t.gif" srcset="//as01.epimg.net/t.gif 200w"/>
            </span>
            <span class="nombre-equipo" itemprop="name">M. City</span>
        </a>
    </div>
    <div class="info-evento">
        <span class="info-evento-int">
            <ul class="bullet-list">
                <li class="cont-fecha">
                    <span>
                        <span class="icono as-icon-calendario"></span>
                        <span class="fecha">Su-07/08 11:30</span>
                    </span>
                </li>
            </ul>
        </span>
        <span content="Su-07/08 11:30 West Ham - M. City" itemprop="name"></span>
        <time content="2022-08-07T15:30:00+00:00" itemprop="startDate"></time>
        <span itemprop="location" itemscope="" itemtype="http://schema.org/StadiumOrArena">
            <span content="" itemprop="name"></span>
            <span content="" itemprop="address"></span>
            <span itemprop="geo" itemscope="" itemtype="http://schema.org/GeoCoordinates">
                <meta content="" itemprop="latitude"/>
                <meta content="" itemprop="longitude"/>
            </span>
        </span>
    </div>
</li>
'''
en_as_com_url = "https://en.as.com/resultados/futbol/inglaterra/2022_2023/jornada/regular_a_"

# Helper method(s)
def readJSONFile(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

# Read input from command line
parser = argparse.ArgumentParser(description='Scrape fixture data from a website and save it to a local file.')
parser.add_argument('-f', '--file', required=True,
        help='Filename of the fixtures to be updated')
args = parser.parse_args()

all_fixtures = []
# en.as.com has gameweek specific fixture URLs, need to append gameweek # to URL
for gameweek in range(1, 39):
    url = en_as_com_url + str(gameweek)
    soup = BeautifulSoup(requests.get(url).text, features="html.parser")
    fixtures = soup.find_all('li', "list-resultado")
    for fixture in fixtures:
        home_team = fixture.find("div", "equipo-local").find("span", "nombre-equipo").string
        away_team = fixture.find("div", "equipo-visitante").find("span", "nombre-equipo").string
        game_datetime_utc = fixture.find("time", attrs={"itemprop": "startDate"})['content'].split('+')[0]
        fixture_obj = {"home": home_team, "away": away_team, "datetime_utc": game_datetime_utc}
        all_fixtures.append(fixture_obj)

    # Sleep for 5 seconds so that we don't get flagged by the website
    print("Finished with Gameweek {}, sleeping for 5 seconds...".format(gameweek))
    time.sleep(5)

file_fixtures = readJSONFile(args.file)

for fixture in all_fixtures:
    if fixture not in file_fixtures:
        print("New fixture to add: {}".format(fixture))
for fixture in file_fixtures:
    if fixture not in all_fixtures:
        print("Old fixture to remove: {}".format(fixture))

# Save to local file (for now)
fixture_filename = args.file
print("Done, dumping to {}".format(fixture_filename))
with open(fixture_filename, 'w') as fixture_file:
    json.dump(all_fixtures, fixture_file)


