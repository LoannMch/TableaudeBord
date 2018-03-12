import pandas as pd
import json
import os
import glob

import pyodbc

# LAPTOP-4H4QSG7A\SQLEXPRESS
#con = pyodbc.connect("Driver={SQL Server};"
#                     "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
#                    "Database=master;"
#                     "Trusted_Connection=yes;")

#cursor = con.cursor()
#cursor.execute('SELECT * FROM country')

con = None

def call_procedure(con, data, file_name):
	try : 
		# Here we insert data 
		data = pd.DataFrame.from_dict(data)


		# If calling procedure is ok : rename fil as txt
		#os.rename(file, '{}/norse_json/{}.txt'.format(cwd,file_name))

	except : 
		log.error('Error for file : {}'.format(file_name))


if __name__ == '__main__':
	cwd = os.getcwd()

	list_file = glob.glob("{}/norse_json/*.json".format(cwd))

	for file in list_file : 

		file_name = file.split('/')[-1].split('.json')[0]

		with open(file) as json_data:
			data = json.load(json_data)
		
		call_procedure(con, data, file_name)
		
		# To do rename with txt 	
		print('File analyzed : {}'.format(file_name))
		
		#os.rename(file, '{}/norse_json/A{}.json'.format(cwd,file_name))
		