import pandas as pd
import json
import os
import glob

import pyodbc

# LAPTOP-4H4QSG7A\SQLEXPRESS
con = pyodbc.connect("Driver={SQL Server};"
                     "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                     "Database=master;"
                     "Trusted_Connection=yes;")

cursor = con.cursor()
cursor.execute('SELECT * FROM country')


for row in cursor:
    # print(row)
    print('row = %r' % (row,))


def call_procedure()

def

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