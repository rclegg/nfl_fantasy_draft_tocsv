import config
from util import get_soup as gs
import csv

league_id = config.LEAGUE_ID

league_settings_soup = gs.get_league_settings(league_id)

league_settings = league_settings_soup.find_all('div')

# Get the number of Teams in the League from Settings
for i in league_settings:
    if i.previous == 'Teams':
        Number_of_Teams = i.contents[0]

team_id_numbers = range(1, int(Number_of_Teams) + 1)

player_dict = {}

for team_id_number in team_id_numbers:
    team_page = gs.get_team_roster_by_team_id(league_id, team_id_number)
    team_page_players = team_page.find_all('a', class_='playerCard')

    for i in team_page_players:
        player_id = int(i.attrs['href'].split('playerId=')[1])
        if str(i.contents[0]) != 'View News':
            player_name = str(i.contents[0])
        # draft_position = i.parent.parent.contents[0].contents[0].split('.')[0]
        # draft_round = i.parent.parent.contents[0].parent.parent.parent.contents[0].contents[0].split(' ')[1]
        # fantasy_team = i.parent.parent.contents[6].text
        player_dict.update({player_id: {"PlayerName": player_name,
                                        "TeamIdNumber": team_id_number}})

with open('nfl_fantasy_player_rosters.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['player_id', 'PlayerName', 'TeamIdNumber'])  # Create Header
    for k, v in player_dict.items():
        writer.writerow([k, v['PlayerName'], v['TeamIdNumber']])
