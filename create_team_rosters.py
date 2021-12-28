from util import get_soup as gs
import csv
import config

LEAGUE_ID = config.LEAGUE_ID


def get_number_of_teams(league_id: int):
    league_settings_soup = gs.get_league_settings(league_id)

    league_settings = league_settings_soup.find_all('div')

    # Get the number of Teams in the League from Settings
    for i in league_settings:
        if i.previous == 'Teams':
            number_of_teams = i.contents[0]

            team_id_numbers = range(1, int(number_of_teams) + 1)

            return team_id_numbers


def get_fantasy_team_names(league_id):
    league_home_soup = gs.get_league_home(league_id)

    league_home_team_names = league_home_soup.find_all('a', class_='teamName')

    fantasy_team_names_dict = {}

    for i in league_home_team_names:
        fantasy_team_names_dict[int(i.attrs['href'].split('/')[-1:][0])] = i.contents[0]

    return fantasy_team_names_dict


def create_team_rosters_dict(league_id: int, number_of_teams: range):
    player_dict = {}

    for team_id_number in number_of_teams:
        team_page = gs.get_team_roster_by_team_id(league_id, team_id_number)
        team_page_players = team_page.find_all('a', class_='playerCard')

        for i in team_page_players:
            player_id = int(i.attrs['href'].split('playerId=')[1])
            if str(i.contents[0]) != 'View News':
                player_name = str(i.contents[0])
                player_dict.update({player_id: {"PlayerName": player_name,
                                                "FantasyTeamId": team_id_number}})

    return player_dict


def export_team_rosters_to_csv(team_rosters: dict):
    with open('nfl_fantasy_player_rosters.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # Create Header
        writer.writerow(['player_id',
                         'PlayerName',
                         'FantasyTeamId'])
        # Write Data
        for k, v in team_rosters.items():
            writer.writerow(
                            [k,
                             v['PlayerName'],
                             v['FantasyTeamId']])


def main():
    id_numbers = get_number_of_teams(LEAGUE_ID)
    team_rosters_dict = create_team_rosters_dict(LEAGUE_ID, id_numbers)
    export_team_rosters_to_csv(team_rosters_dict)
