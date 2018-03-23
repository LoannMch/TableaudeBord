import pandas as pd
import json
import os
import glob
import datetime
import pyodbc


def call_procedure(con, data, file_name):
    #print(len(data))
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].apply(lambda x : update_date(x))
    data['Notify'] = data['Notify'].apply(lambda x : x.lower() if x == x else x)
    data['Country'] = data['Country'].apply(lambda x : x.lower() if x == x else x)
    data['retrieveCountry'] = data['retrieveCountry'].apply(lambda x : x.lower() if x == x else '')
    data['retrieveIndustry'] = data['retrieveIndustry'].apply(lambda x : x.lower() if x == x else '')
    # data['Famous'] = data['retrieveIndustry'].apply(lambda x : x == x )
    # data['Famous'] = data['retrieveIndustry'].apply(lambda x : 1 if(x == x) else 0 )
    data.apply(procedure_insert, axis = 'columns')
    #print(data['Famous'].unique())
    
def update_date(x):
    return('{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}'.format(x.day, x.month, x.year, x.hour, x.minute, x.second))

def procedure_insert(row):
    
    sql = 'exec InsertDataFromZoneH  @attacker = \'' + row['Notify'] + '\', \
    @date = \'' + row['Date']  + '\', \
    @lib_organisation = \'' + row['company'] + '\', \
    @lib_type_server = \'' + row['WebServer'] + '\', \
    @country = \'' + row['retrieveCountry'] + '\', \
    @lib_OS_property = \'' + row['OS'] + '\', \
    @type_organisation = \'' + row['retrieveIndustry'] + '\''
    
    #print(sql)

    '''
    print(row['Date'])
    print(row['Notify'])
    print(row['retrieveCountry'])
    # print(data['Famous'])
    print(row['OS'])
    print(row['WebServer'])
    print(row['company'])
    print(row['retrieveIndustry'])'''
    

    cursor = con.cursor()
    cursor.execute(sql)
    cursor.commit()

if __name__ == '__main__':

    con = pyodbc.connect("Driver={SQL Server};"
    						"Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
    						"Database=master;"
    						"Trusted_Connection=yes;")

    # cwd = os.getcwd()
    # list_file = glob.glob("./../data/*0.csv".format(cwd))
    list_file = ['./../data/myData_TEST.csv']

    for file in list_file : 
        file_name = file.split('/')[-1].split('.csv')[0]
        data = pd.read_csv(file, low_memory=False, encoding='latin-1')
        d = data[:2].copy()
        # print(d)
        call_procedure(con, d, file_name)
        print('File analyzed : {}'.format(file_name))

        
#print('test' , ' h')