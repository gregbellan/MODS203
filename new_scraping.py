import urllib.request
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

file_games_data = './game_ID_df.csv'
run = True

list_games_ID = np.array(pd.read_csv('./list_ID_games.csv'))
while run:
	# columns = ['Game ID', 'Genres', 'Developers', 'Release date', 'Current price', 'Number of reviews', 'Positive rate in reviews', 'SteamDB score', 'Minimum requirements', 'Recommended requirements']
	games_df = pd.read_csv(file_games_data)

	if len(games_df.index) == 0:
		previous_end = None
	else:
		previous_end = games_df.iloc[-1][0]
	print(previous_end)

	if previous_end is None:
		start_index = 0
	else:
		start_index = np.where(list_games_ID == previous_end)[0][0] + 1
	
	if start_index == len(list_games_ID):
		run = False
		break
	print(start_index)
	
	for app_ID in list_games_ID[start_index:start_index+200]:
		app_ID = app_ID[0]
		minimum_req = {}
		recommended_req = {}
		genres = []
		developer_list = None
		publisher_list = None
		url_game_info = 'https://store.steampowered.com/api/appdetails?appids={}'.format(app_ID)
		url_reviews = 'https://store.steampowered.com/appreviews/{}?json=1&language=all&purchase_type=all&day_range=all'.format(app_ID)
		try:
			app_info = urllib.request.urlopen(url_game_info)
			reviews_info = urllib.request.urlopen(url_reviews)
		except Exception as e:
			print('Error with urlopen while scraping\n')
			print(str(e))
			continue
		app_data_dict = json.loads(app_info.read().decode())
		reviews_info_dict = json.loads(reviews_info.read().decode())
		if app_data_dict['{}'.format(app_ID)]['success']:
			raw_game_data = app_data_dict['{}'.format(app_ID)]['data']
			useful_reviews_data = reviews_info_dict['query_summary']
			if 'pc_requirements' in raw_game_data:
				if type(raw_game_data['pc_requirements']) is not list:
					min_recom = ['minimum', 'recommended']
					for detail in min_recom:
						if detail in raw_game_data['pc_requirements']:
							requirements = raw_game_data['pc_requirements'][detail]
							bs = BeautifulSoup(requirements, 'html.parser')
							if bs.find('ul', 'bb_ul') is not None:
								list_components_requirements_min = bs.find('ul', 'bb_ul').findAll('li')
							elif bs.find('ul') is not None:
								list_components_requirements_min = bs.find('ul').findAll('li')
							else:
								list_components_requirements_min = None
							if list_components_requirements_min is not None:
								for li in list_components_requirements_min:
									if li.find('strong') is not None:
										if detail == 'minimum':
											minimum_req[li.contents[0].contents[0]] = li.contents[1]
										else:
											recommended_req[li.contents[0].contents[0]] = li.contents[1]
				else:
					continue
			else:
				continue
			if 'genres' in raw_game_data:
				genres_list_dict = raw_game_data['genres']
				for items in genres_list_dict:
					genres.append(items['description'])
			if 'developers' in raw_game_data:
				developer_list = raw_game_data['developers']
			if 'publishers' in raw_game_data:
				publisher_list = raw_game_data['publishers']
			if 'price_overview' in raw_game_data:
				price = raw_game_data['price_overview']['final_formatted']
			else:
				price = 'Free'
			release_date = raw_game_data['release_date']['date']
			total_reviews, positive_reviews = useful_reviews_data['total_reviews'], useful_reviews_data['total_positive']
			if total_reviews != 0:
				positive_rate = str(round(positive_reviews / total_reviews * 100)) + '%'
			else:
				positive_rate = '0%'
			steam_db_score = None
			item = {
				'Game ID': app_ID,
				'Genres': genres,
				'Developers': developer_list,
				'Publishers': publisher_list,
				'Release date': release_date,
				'Current price': price,
				'Number of reviews': total_reviews,
				'Positive rate in reviews': positive_rate,
				'SteamDB score': steam_db_score,
				'Minimum requirements': minimum_req,
				'Recommended requirements': recommended_req
			}
			games_df = games_df.append(item, ignore_index=True)
		
	games_df.to_csv(file_games_data, mode='w', index=False)
	time.sleep(5*60)