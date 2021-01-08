import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
import json

from pandas.core.frame import DataFrame

url = 'https://store.steampowered.com/api/appdetails?appids=224380'
app_info = urllib.request.urlopen(url)
app_info_dict = json.loads(app_info.read().decode())

#minimum_req = {'OS':None, 'Processor':None, 'Memory':None, 'Graphics':None, 'Storage':None, 'Sound Card':None}
minimum_req = {}

requirements = app_info_dict['224380']['data']['pc_requirements']['minimum']
bs = BeautifulSoup(requirements, 'html.parser')
doc = html.fromstring(requirements)

list_components_requirements = bs.find('ul').findAll('li')
for li in list_components_requirements:
	if li.find('strong') is not None:
		minimum_req[li.contents[0].contents[0]] = li.contents[1]
score = 0
release_date = '12 dec 2020'
game_ID = 43535636
price = '12,99€'
total_reviews = 14444
positive_rate = '90%'
metacritic_score = 71

columns = ['Game ID', 'Release date', 'Current price', 'Number of reviews', 'Positive rate in reviews', 'Metacritic score', 'Minimum requirements']

df = DataFrame(columns=columns)
df.to_csv('./test_1.csv', index=False)
item = {
                'Game ID': game_ID,
                'Release date': release_date,
                'Current price': price,
                'Number of reviews': total_reviews,
                'Positive rate in reviews': positive_rate,
                'Metacritic score': metacritic_score,
                'Minimum requirements': minimum_req
            }
df = df.append(item, ignore_index=True)
df = df.append(item, ignore_index=True)
df = df.append(item, ignore_index=True)
df = df.append(item, ignore_index=True)
df.to_csv('./test_1.csv', mode='a', index=False, header=None)