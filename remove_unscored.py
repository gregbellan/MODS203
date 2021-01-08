import numpy as np
import pandas as pd

all_data_df = pd.read_csv('./all_data_scraped.csv')
scores = np.array(all_data_df['SteamDB score'])
price = np.array(all_data_df['Current price'])
compteur = 0
for game_score in scores:
	if game_score == '-1':
		compteur += 1
print('{} rows must be deleted. The new shape is: {}'.format(compteur, len(all_data_df)-compteur))
data_with_score_df = all_data_df[all_data_df['SteamDB score'] != '-1']

# some games do not have their prices in euros so we delete these observations as we cannot compare them with the others
for i in range(len(price)):
	if price[i] != 'Free' and '€' not in price[i]:
		data_with_score_df = data_with_score_df.drop(labels=i, axis=0)
print('The final size is {}'.format(len(data_with_score_df)))

data_with_score_df.to_csv('./data_with_scores.csv', mode='w', index=False)