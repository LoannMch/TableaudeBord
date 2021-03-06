import pandas as pd
import json
import os
import glob
import pyodbc


def procedure_insert(row):
    """
	 Entrée: 
         row is a dictionnary which have key and value 
    """
    sql = 'exec InsertDataFromNorse @type_attack=\'' + row['attack_type'] \
            + '\',@target_country=\'' + row['target_country'] \
            + '\',@target_town=\'' + row['target_town'] \
            + '\',@attacker_town=\''+row['attacker_town'] \
            + '\',@attacker_country=\''+row['attacker_country'] \
            +'\',@attacker=\''+row['attacker'] + '\',@date=\'' \
            + row['date']+'\''
    cursor = con.cursor()
    cursor.execute(sql)
    cursor.commit()


def update_date(x):
    """
        Entrée:
            x is a pandas datetime object
        Sorties:
            string
        this fonction allow to return string at the well date format
    """
    return('{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}'.format(x.day, x.month, 
           x.year, x.hour, x.minute, x.second))


def call_procedure(con, data, file_name, mapping_country):
    """
        Entrée:
            con : object which allow connection to the database
            data : dataframe which contains data
            file_name : file of the dataframe data
        mapping_country : dictionnary which allow to convert code
        of the country as label
    """

    data = pd.DataFrame.from_dict(data)
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].apply(lambda x : update_date(x))

    data['attacker_country'] = data['attacker_country'].apply(
            lambda x : x.replace(x, mapping_country[x]))
    data['target_country'] = data['target_country'].apply(
            lambda x : x.replace(x, mapping_country[x]))

    data.apply(procedure_insert, axis = 'columns')

    
if __name__ == '__main__':
    
    mapping_country = {
	    'NL': 'netherlands',
	    'CN': 'china',
	    'US': 'united states',
	    'MX': 'mexico',
	    'TR': 'turkey',
	    'PK': 'pakistan',
	    'HK': 'hong kong',
	    'VN': 'vietnam',
	    'RO': 'roumania',
	    'IT': 'italy',
	    'KR': 'south korea',
	    'JP': 'japan',
	    'CH': 'swiss',
	    'UA': 'ukraine',
	    'ES': 'spain',
	    'CZ': 'czech republic',
	    'BR': 'brazil',
	    'IN': 'india',
	    'PH': 'philippines',
	    'GB': 'united kingdom',
	    'PL': 'poland',
	    'FR': 'france',
	    'IL': 'israel',
	    'CA': 'canada',
	    'CO': 'colombia',
	    'DE': 'germany',
	    'SA': 'saudi arabia',
	    'AM': 'armenia',
	    'BO': 'bolivia',
	    'BG': 'bulgaria',
	    'AR': 'argentina',
	    'TW': 'taiwan',
	    'MD': 'moldova',
	    'ID': 'indonesia',
	    'BE': 'belgium',
	    'TH': 'thailand',
	    'PT': 'portugal',
	    'EG': 'egypt',
	    'CL': 'chile',
	    'NZ': 'new zealand',
	    'RU': 'russia',
	    'CY': 'cyprus',
	    'BM': 'bermuda',
	    'MN': 'mongolia',
	    'IR': 'ireland',
	    'BD': 'bangladesh',
	    'SI': 'slovenia',
	    'VE': 'venezuela',
	    'AU': 'australia',
	    'AE': 'united arab emirates',
	    'NO': 'norway',
	    'SG': 'singapore',
	    'IE': 'ireland',
	    'IS': 'iceland',
	    'AT': 'austria'    
    }
    
    con = pyodbc.connect("Driver={SQL Server};"
                            "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                            "Database=master;"
                            "Trusted_Connection=yes;")

    cwd = os.getcwd()
    list_file = glob.glob("{}/norse_json/*.json".format(cwd))
    # For each json file of the selected directory :
    for file in list_file: 
        file_name = file.split('/')[-1].split('.json')[0]
        # Reading the csv file in json_data
        with open(file) as json_data:
        	# Convert json_data as pandas dataframe
            data = json.load(json_data)
            call_procedure(con, data, file_name, mapping_country)
        print('File analyzed : {}'.format(file_name))

		