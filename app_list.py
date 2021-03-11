import urllib.request
import pandas as pd
import json
import time
import numpy as np

file_ID_games = './list_ID_games.csv'
file_ID_apps = './list_ID_apps.csv'

"""
list_apps_ID = urllib.request.urlopen('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
apps_ID_dict = json.loads(list_apps_ID.read().decode())
for app_dict in apps_ID_dict['applist']['apps']:
	app_ID = app_dict['appid']
	app_ID_df = app_ID_df.append({'App ID': app_ID}, ignore_index=True)

app_ID_df.to_csv(file_ID_apps, mode='w', index=False)
"""

run = True

apps_IDs = np.array(pd.read_csv(file_ID_apps))
while run:
	game_ID_df = pd.read_csv(file_ID_games)

	if len(game_ID_df.index) == 0:
		previous_end = None
	else:
		previous_end = game_ID_df.iloc[-1][0]
	print(previous_end)
	
	if previous_end is None:
		start_index = 0
	else:
		start_index = np.where(apps_IDs == previous_end)[0][0] + 1
	
	if start_index == len(apps_IDs):
		run = False
		break
	print(start_index)

	for app_ID in apps_IDs[start_index:start_index+200]:
		app_ID = app_ID[0]
		
		url_game_info = 'https://store.steampowered.com/api/appdetails?appids={}'.format(app_ID)
		try:
			app_info = urllib.request.urlopen(url_game_info)
		except Exception as e:
			print('Error in urlopen\n')
			print(str(e))
			continue
		app_data_dict = json.loads(app_info.read().decode())
		if app_data_dict['{}'.format(app_ID)]['success']:
			if app_data_dict['{}'.format(app_ID)]['data']['type'] == 'game':
				game_ID_df = game_ID_df.append({'Game ID': app_ID}, ignore_index=True)

	game_ID_df.to_csv(file_ID_games, mode='w', index=False)
	time.sleep(5*60)