import numpy as np
import pandas as pd

games_ID_array = np.array(pd.read_csv('list_ID_games.csv'))
games_ID_with_data = np.array(pd.read_csv('game_ID_df.csv')['Game ID'])
if len(games_ID_array)!= len(games_ID_with_data):
	print('Some values are missing')
else:
	for i in range(len(games_ID_array)):
		if games_ID_array[i][0] != games_ID_with_data[i]:
			print('found a missing value: index={} and game ID={}'.format(i, games_ID_with_data))
	print('No games were lost in the scraping')