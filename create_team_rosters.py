import csv
import NFLSoup
import config

"""Creates a CSV of up-to-date or season-end rosters for each fantasy team in the league."""

LEAGUE_ID = config.LEAGUE_ID
SEASON_END_YEAR = config.SEASON_END_YEAR


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
    rosters = NFLSoup.NFLFantasyFootballTeams(league_id=LEAGUE_ID,
                                              season_end_year=SEASON_END_YEAR).create_team_rosters()
    export_team_rosters_to_csv(rosters)


main()
