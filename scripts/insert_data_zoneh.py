import pandas as pd
import json
import os
import glob
import datetime
import pyodbc

def call_procedure(con, data, file_name):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].apply(lambda x : update_date(x))
    data['Notify'] = data['Notify'].apply(lambda x : x.lower() if x == x else x)
    data['Country'] = data['Country'].apply(lambda x : x.lower() if x == x else x)
    data['Famous'] = data['retrieveIndustry'].apply(lambda x : x == x )
    #data.apply(procedure_insert, axis = 'columns')

def update_date(x):
    return('{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}'.format(x.day, x.month, x.year, x.hour, x.minute, x.second))

def procedure_insert(row):
    #sql = 'exec InsertDataFromNorse @type_attack=\''+row['attack_type']+'\',@target_country=\''+row['target_country']+'\',@target_town=\''+row['target_town']+'\',@attacker_town=\''+row['attacker_town']+'\',@attacker_country=\''+row['attacker_country']+'\',@attacker=\''+row['attacker']+'\',@date=\''+row['date']+'\''
    #sql :
    cursor = con.cursor()
    cursor.execute(sql)
    cursor.commit()

if __name__ == '__main__':

	con = pyodbc.connect("Driver={SQL Server};"
						"Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
						"Database=master;"
						"Trusted_Connection=yes;")

	cwd = os.getcwd()
	list_file = glob.glob("./../data/*0.csv".format(cwd))

	for file in list_file : 
		
		file_name = file.split('/')[-1].split('.csv')[0]
		
		data = pd.read_csv(file, low_memory=False, encoding='latin-1')
		
		call_procedure(con, data, file_name)

		print('File analyzed : {}'.format(file_name))