import pandas as pd
import numpy as np
import ast

datafile = './all_data_scraped.csv'
games_data_df = pd.read_csv(datafile)
requirements = np.array(games_data_df['Minimum requirements'])
recom_conf = np.array(games_data_df['Recommended requirements'])
all_configs_df = pd.DataFrame(columns=['Min configuration class'])
new_requirements_list = []
# keep only the useful information about the minimum requirements
"""
for game_requirement in requirements:
	reshaped_requirements = {}
	game_requirement_dict = ast.literal_eval(game_requirement)
	if 'Processor:' in game_requirement_dict:
		reshaped_requirements['Processor'] = game_requirement_dict['Processor:'].lower()
	else:
		reshaped_requirements['Processor'] = 'Not specified'
	if 'Memory:' in game_requirement_dict:
		reshaped_requirements['Memory'] = game_requirement_dict['Memory:'].upper()
	else:
		reshaped_requirements['Memory'] = 'Not specified'
	if 'Graphics:' in game_requirement_dict:
		reshaped_requirements['Graphics'] = game_requirement_dict['Graphics:']
	else:
		reshaped_requirements['Graphics'] = 'Not specified'
	new_requirements_list.append(reshaped_requirements)
games_data_df['Minimum requirements'] = new_requirements_list
games_data_df.to_csv(datafile, mode='w', index=False)
"""
# same for the recommended configuration
"""
for game_recom_conf in recom_conf:
	reshaped_requirements = {}
	game_requirement_dict = ast.literal_eval(game_recom_conf)
	if game_requirement_dict != {}:
		if 'Processor:' in game_requirement_dict:
			reshaped_requirements['Processor'] = game_requirement_dict['Processor:'].lower()
		else:
			reshaped_requirements['Processor'] = 'Not specified'
		if 'Memory:' in game_requirement_dict:
			reshaped_requirements['Memory'] = game_requirement_dict['Memory:'].upper()
		else:
			reshaped_requirements['Memory'] = 'Not specified'
		if 'Graphics:' in game_requirement_dict:
			reshaped_requirements['Graphics'] = game_requirement_dict['Graphics:']
		else:
			reshaped_requirements['Graphics'] = 'Not specified'
		new_requirements_list.append(reshaped_requirements)
	else:
		new_requirements_list.append({})
games_data_df['Recommended requirements'] = new_requirements_list
games_data_df.to_csv(datafile, mode='w', index=False)"""

# compute configuration class for each observation based on the minimum requirements

for game_requirement in requirements:
	config_class = 0
	game_requirement_dict = ast.literal_eval(game_requirement)
	processor = game_requirement_dict['Processor']
	memory = game_requirement_dict['Memory']
	if processor != 'Not specified':
		if ('i3' in processor or 'dual core' in processor or 'single core' in processor) and game_requirement_dict['Graphics'] != 'Not specified':
			config_class = 1
		if memory != 'Not specified':
			if 'i5' in processor and 'MB' in memory:
				config_class = 1
			elif '8 GB' in memory:
				if ('i5' in processor or 'i7' in processor) and '8 GB' in memory:
					config_class = 3
				else:
					config_class = 2
			elif 'i5' in processor and 'GB' in memory:
				config_class = 2
	
	all_configs_df = all_configs_df.append({'Min configuration class': config_class}, ignore_index=True)

games_data_df['Min configuration class'] = all_configs_df
games_data_df.to_csv(datafile, mode='w', index=False)