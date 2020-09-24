import sys

import numpy as np
import pandas as pd

# nba_api
from pandas import DataFrame
from pandas import ExcelWriter
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats


# get_player_shotchartdetail: player_name, season_id -> player_shotchart_df, league_avg
def get_player_shotchartdetail(player_name, season_id):

    # player dictionary
    nba_players = players.get_players()
    player_dict = [
        player for player in nba_players if player['full_name'] == player_name][0]

    # career dataframe
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]

    # team id during the season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    # shotchartdetail endpoints
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                    player_id=int(
                                                        player_dict['id']),
                                                    season_type_all_star='Playoffs',
                                                    season_nullable=season_id,
                                                    context_measure_simple="FGA").get_data_frames()

    return shotchartlist[0]


if __name__ == "__main__":
    df = pd.DataFrame(get_player_shotchartdetail("LeBron James", "2019-20"))
    df.to_csv(r'test.csv',
              index=None, header=True)
    print(df)
