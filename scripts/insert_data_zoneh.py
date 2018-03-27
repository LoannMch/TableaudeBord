# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 19:34:10 2018

@author: Loann
"""

import pandas as pd
import numpy as np
import pyodbc


def call_procedure(con, data, file_name):
    """
        Entrée:
            con : object which allow connection to the database
            data : dataframe which contains data
            file_name : file of the dataframe data
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].apply(lambda x: update_date(x))
    data['Notify'] = data['Notify'].apply(lambda x: x.lower() if x == x else x)
    data['Country'] = data['Country'].apply(
            lambda x: x.lower() if x == x else x)
    data['retrieveCountry'] = data['retrieveCountry'].apply(
            lambda x: x.lower() if x == x else '')
    data['retrieveIndustry'] = data['retrieveIndustry'].apply(
            lambda x: x.lower() if x == x else '')
    data['Famous'] = data['retrieveIndustry'].apply(
            lambda x: x == x)
    data['Famous'] = data['retrieveIndustry'].apply(
            lambda x: 1 if(x == x) else 0)
    data.apply(procedure_insert, axis='columns')


def update_date(x):
    """
        Entrée:
            x is a pandas datetime object
        Sorties:
            string
        this fonction allow to return string at the well date format
    """
    return('{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}'.format(
            x.day, x.month, x.year, x.hour, x.minute, x.second))


def procedure_insert(row):
    notify = is_null(row['Notify'])
    company = is_null(row['company'])
    web_server = is_null(row['WebServer'])
    country = is_null(row['retrieveCountry'])
    os = is_null(row['OS'])
    retrieveIndustry = is_null(row['retrieveIndustry'])
    print(row.name)
    sql = 'exec InsertDataFromZoneH  @attacker ='+notify+', \
    @date = \''+row['Date']+'\', \
    @lib_organisation =' + company + ', \
    @lib_type_server =' + web_server + ', \
    @country ='+country+', \
    @lib_OS_property =' + os + ', \
    @type_organisation =' + retrieveIndustry
    # print(row['Date'])
    # print(row['Notify'])
    # print(row['retrieveCountry'])
    # print(data['Famous'])
    # print(row['OS'])
    # print(row['WebServer'])
    # print(row['company'])
    # print(row['retrieveIndustry'])
    cursor = con.cursor()
    cursor.execute(sql)
    cursor.commit()


def is_null(x):
    """
        Entrée:
            x string
        Sorties:
            string
    """
    if x == 'null':
        return x
    else:
        return '\'' + x + '\''


def referenced_country(x):
    """
        Entrée:
            x string
        Sorties:
            string or np.nan
    """
    if x in mapping_country:
        return x
    else:
        return np.nan


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
        'IT': 'italia',
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
    mapping_country = list(mapping_country.values())
    con = pyodbc.connect("Driver={SQL Server};"
                         "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                         "Database=master;"
                         "Trusted_Connection=yes;")
    # cwd = os.getcwd()
    # list_file = glob.glob("./../data/*0.csv".format(cwd))
    # list_file = ['./../data/DataColumnsClean.csv']
    file = './../data/DataColumnsClean.csv'
    file_name = file.split('/')[-1].split('.csv')[0]
    data = pd.read_csv(file, low_memory=False, encoding='latin-1')
    data['Country'] = data['Country'].replace(np.nan, 'UNKNOWN')
    data['Country'] = data['Country'].apply(lambda x: x.lower())
    data['Country'] = data['Country'].apply(
            lambda x: referenced_country(x))
    data['retrieveCountry'] = data['retrieveCountry'].replace(
            'unknown ', np.nan)
    data['retrieveCountry'] = data['retrieveCountry'].fillna(
            data['Country'])
    data = data.replace('unknown', 'null')
    data = data.replace('Unknown', 'null')
    data = data.fillna('null')
    call_procedure(con, data, file_name)
    print('File analyzed : {}'.format(file_name))
