import pandas as pd
import json
import os
import glob
import datetime
import pyodbc


def procedure_insert(row):
    
    sql = 'exec InsertDataFromNorse @type_attack=\''+row['attack_type']+'\',@target_country=\''+row['target_country']+'\',@target_town=\''+row['target_town']+'\',@attacker_town=\''+row['attacker_town']+'\',@attacker_country=\''+row['attacker_country']+'\',@attacker=\''+row['attacker']+'\',@ip=\''+row['ip']+'\',@date=\''+row['date']+'\''
    print(sql)
    cursor = con.cursor()
    cursor.execute(sql)
    cursor.commit()
    
    print(row['attack_type'])
    print(row['attacker'])
    
    print(row['attacker_country'])
    print(row['target_country'])
    
    print(row['target_town'])
    print(row['attacker_town'])
       
    print(row['date'])
    print(row['ip'])

  
def update_date(x):
    return('{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}'.format(x.day, x.month, x.year, x.hour, x.minute, x.second))


def call_procedure(con, data, file_name, mapping_country):

	#try : 
		# Here we insert data 
    data = pd.DataFrame.from_dict(data)
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].apply(lambda x : update_date(x))

	data['attacker_country'] = data['attacker_country'].apply(lambda x : x.replace(x, mapping_country[x]))
	data['target_country'] = data['target_country'].apply(lambda x : x.replace(x, mapping_country[x]))

    data.apply(procedure_insert, axis = 'columns')

    os.rename(file, '{}/norse_json/{}.txt'.format(cwd,file_name))

		# If calling procedure is ok : rename fil as txt
	

	#except : 
	#	log.error('Error for file : {}'.format(file_name))


if __name__ == '__main__':

	mapping_country = {
	    'NL' : 'netherlands', 
	    'CN' : 'china', 
	    'US' : 'united states', 
	    'MX' : 'mexico', 
	    'TR' : 'turkey', 
	    'PK' : 'pakistan', 
	    'HK' : 'hong kong', 
	    'VN' : 'vietnam', 
	    'RO' : 'roumania', 
	    'IT' : 'italia', 
	    'KR' : 'south korea',
	    'JP' : 'japan', 
	    'CH' : 'swiss', 
	    'UA' : 'ukraine', 
	    'ES' : 'spain', 
	    'CZ' : 'czech republic', 
	    'BR' : 'brazil', 
	    'IN' : 'india', 
	    'PH' : 'philippines', 
	    'GB' : 'united kingdom', 
	    'PL' : 'poland', 
	    'FR' : 'france', 
	    'IL' : 'israel', 
	    'CA' : 'canada', 
	    'CO' : 'colombia', 
	    'DE' : 'germany', 
	    'SA' : 'saudi arabia', 
	    'AM' : 'armenia', 
	    'BO' : 'bolivia', 
	    'BG' : 'bulgaria', 
	    'AR' : 'argentina', 
	    'TW' : 'taiwan', 
	    'MD' : 'moldova',
	    'ID' : 'indonesia', 
	    'BE' : 'belgium', 
	    'TH' : 'thailand', 
	    'PT' : 'portugal', 
	    'EG' : 'egypt', 
	    'CL' : 'chile', 
	    'NZ' : 'new zealand', 
	    'RU' : 'russia', 
	    'CY' : 'cyprus', 
	    'BM' : 'bermuda', 
	    'MN' : 'mongolia',
	    'IR' : 'ireland', 
	    'BD' : 'bangladesh', 
	    'SI' : 'slovenia', 
	    'VE' : 'venezuela', 
	    'AU' : 'australia', 
	    'AE' : 'united arab emirates',
	    'NO' : 'norway',
	    'SG' : 'singapore',
	    'IE' : 'ireland',
	    'IS' : 'iceland',
	    'AT' : 'austria'    
	}

    con = pyodbc.connect("Driver={SQL Server};"
                             "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                             "Database=master;"
                             "Trusted_Connection=yes;")
    cwd = os.getcwd()
    list_file = glob.glob("{}/norse_json/*.json".format(cwd))
    list_file = ['E:/M1SID/S8/Projet_TableaudeBord/Hacking/TableaudeBord/scripts/norse_json/test.json']
    for file in list_file : 
        file_name = file.split('/')[-1].split('.json')[0]
        with open(file) as json_data:
            data = json.load(json_data)
            call_procedure(con, data, file_name, mapping_country)
		
        # To do rename with txt 	
        print('File analyzed : {}'.format(file_name))
		
		#os.rename(file, '{}/norse_json/A{}.json'.format(cwd,file_name))
		