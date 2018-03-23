# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:19:54 2018

@author: Loann
"""

import requests
import pyodbc
import pandas as pd

def export_query_to_csv(sql, columns, name_csv):
    con = pyodbc.connect("Driver={SQL Server};"
                        "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                        "Database=master;"
                        "Trusted_Connection=yes;")
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    tab =[]
    nb_col = len(columns)
    for row in rows:
        col = []
        for i in range(nb_col):
            col.append(row[i])
        tab.append(col)  
    df = pd.DataFrame(tab, columns=columns)
    df.to_csv('CSV_for_analyse/' + name_csv)


sql = 'SELECT count(id_attack) as Nb_attack,lib_type_attack,lib_country \
FROM attack, type_attack, city ,country \
WHERE attack.id_type_attack = type_attack.id_type_attack \
AND attack.id_city = city.id_city \
AND  city.id_country =country.id_country \
GROUP BY lib_type_attack,lib_country \
ORDER BY count(id_attack) DESC;'

columns = ['Nb_attack', 'type_attaque', 'pays_cible']  
export_query_to_csv(sql, columns, 'NbrAttack_type_pays.csv')