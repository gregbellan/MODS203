import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from typing_extensions import final

file_games_IDs = 'list_ID_games.csv'
file_info_games = 'game_ID_df.csv'
user_agent = {'User-agent': 'SteamDB-Educational-Access; victor.manach@telecom-paris.fr'}
game_ID_array = np.array(pd.read_csv(file_games_IDs))

run = True
while run:
	tmp_df = pd.read_csv('./steamDB_scores.csv')

	if len(tmp_df.index) == 0:
		previous_end = None
	else:
		previous_end = tmp_df.iloc[-1][0]
	print(previous_end)

	if previous_end is None:
		start_index = 0
	else:
		start_index = np.where(game_ID_array == previous_end)[0][0] + 1
	
	if start_index == len(game_ID_array):
		run = False
		break
	print(start_index)

	for game_ID in game_ID_array[start_index:start_index+200]:
		game_ID = game_ID[0]
		url = 'https://steamdb.info/app/{}/'.format(game_ID)
		r = requests.get(url, headers=user_agent)
		bs = BeautifulSoup(r.text, 'html.parser')
		if bs.find('a', 'header-thing tooltipped tooltipped-n') is not None:
			steamDB_score_raw = bs.find('a', 'header-thing tooltipped tooltipped-n').find('div', re.compile('header-thing-number header-thing-')).text
			final_score = re.findall("\d+\.\d+", steamDB_score_raw)[0] + '%'
		else:
			final_score = '-1'
		tmp_df = tmp_df.append({'Game ID': game_ID,'SteamDB score': final_score}, ignore_index=True)

	tmp_df.to_csv('./steamDB_scores.csv', mode='w', index=False)