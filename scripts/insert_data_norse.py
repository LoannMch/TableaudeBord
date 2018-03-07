import pandas as pd
import json
import os
import glob


def call_procedure()

if __name__ == '__main__':
	cwd = os.getcwd()

	list_file = glob.glob("{}/norse_json/*.json".format(cwd))

	for file in list_file : 

		file_name = file.split('/')[-1].split('.json')[0]

		with open(file) as json_data:
			data = json.load(json_data)
			
		# To do rename with txt 	
		print('File analyzed : {}'.format(fil_name))
		
		#os.rename(file, '{}/norse_json/A{}.json'.format(cwd,file_name))
		#os.rename(file, '{}/norse_json/A{}.txt'.format(cwd,file_name))