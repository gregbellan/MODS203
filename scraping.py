import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import csv

list_apps_ID = urllib.request.urlopen('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
apps_ID_dict = json.loads(list_apps_ID.read().decode())
games = []
columns = ['Game ID', 'Release date', 'Current price', 'Number of reviews', 'Positive rate in reviews', 'Metacritic score', 'Minimum requirements']
games_df = pd.DataFrame(columns=columns)
i = 0
filename = './game_ID_1.csv'
with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(columns)

for app_dict in apps_ID_dict['applist']['apps']:
    minimum_req = {}
    i += 1
    if i == 10:
        time.sleep(30)
        i = 0
    app_ID = app_dict['appid']
    url_game_info = 'https://store.steampowered.com/api/appdetails?appids={}'.format(app_ID)
    url_reviews = 'https://store.steampowered.com/appreviews/{}?json=1&language=all&purchase_type=all&day_range=all'.format(app_ID)
    app_info = urllib.request.urlopen(url_game_info)
    k, j = 0, 0
    while app_info.status != 200 and k<10:
        app_info = urllib.request.urlopen(url_game_info)
        k += 1
    if k==10:
        continue
    reviews_info = urllib.request.urlopen(url_reviews)
    while reviews_info.status != 200 and j<10:
        reviews_info = urllib.request.urlopen(url_reviews)
        j += 1
    if j==10:
         continue
    app_data_dict = json.loads(app_info.read().decode())
    reviews_info_dict = json.loads(reviews_info.read().decode())
    if app_data_dict['{}'.format(app_ID)]['success']:
        raw_game_data = app_data_dict['{}'.format(app_ID)]['data']
        useful_reviews_data = reviews_info_dict['query_summary']
        if raw_game_data['type'] == 'game':
            if 'pc_requirements' in raw_game_data:
                if type(raw_game_data['pc_requirements']) is not list:
                    requirements = raw_game_data['pc_requirements']['minimum']
                    bs = BeautifulSoup(requirements, 'html.parser')
                    if bs.find('ul', 'bb_ul') is not None:
                        list_components_requirements = bs.find('ul', 'bb_ul').findAll('li')
                    elif bs.find('ul') is not None:
                        list_components_requirements = bs.find('ul').findAll('li')
                    else:
                        list_components_requirements = None
                    if list_components_requirements is not None:
                        for li in list_components_requirements:
                            if li.find('strong') is not None:
                                minimum_req[li.contents[0].contents[0]] = li.contents[1]
                else:
                    continue
            else:
                continue
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
            if 'metacritic' in raw_game_data:
                metacritic_score = raw_game_data['metacritic']['score']
            else:
                metacritic_score = None
            item = {
                'Game ID': app_ID,
                'Release date': release_date,
                'Current price': price,
                'Number of reviews': total_reviews,
                'Positive rate in reviews': positive_rate,
                'Metacritic score': metacritic_score,
                'Minimum requirements': minimum_req
            }
            games_df = games_df.append(item, ignore_index=True)
            with open(filename, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([app_ID, release_date, price, total_reviews, positive_rate, metacritic_score, minimum_req])

games_df.to_csv('./game_ID_df.csv', mode='w', index=False)