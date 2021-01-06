import numpy as np
import pandas as pd

data_df = pd.read_csv('./game_ID_df.csv')
steamDB_scores_df = pd.read_csv('./steamDB_scores.csv')

data_df['SteamDB score'] = steamDB_scores_df['SteamDB score']
data_df.to_csv('./all_data_scraped.csv', mode='w', index=False)