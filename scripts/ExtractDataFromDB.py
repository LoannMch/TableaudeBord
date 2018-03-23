# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:19:54 2018

@author: Loann
"""

import requests
import pyodbc
import pandas as pd


    
sql = 'SELECT count(id_attack) as Nb_attack,lib_country \
FROM attack, city ,country \
WHERE attack.id_city = city.id_city \
AND  city.id_country =country.id_country \
GROUP BY lib_country \
ORDER BY count(id_attack) DESC;'

columns = ['nb_attack', 'country']

def export_query_to_csv(sql, columns, name_csv):
    con = pyodbc.connect("Driver={SQL Server};"
                        "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                        "Database=master;"
                        "Trusted_Connection=yes;")
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    tab =[]
    for row in rows:
        tab.append([row[0], row[1]])  
    df = pd.DataFrame(tab, columns=columns)
    df.to_csv('CSV_for_analyse/' + name_csv)
  
export_query_to_csv(sql, columns, 'pays_attaqué.csv')