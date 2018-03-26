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


sql = 'SELECT c.lib_country, \
(SELECT count(id_attack) as Nb_attack_subie \
FROM attack, city ,country \
WHERE attack.id_city = city.id_city \
AND city.id_country = country.id_country \
AND country.lib_country = c.lib_country \
GROUP BY lib_country) as Nb_attack_subie, \
(SELECT count(id_attack) as Nb_attack_emmise \
FROM attack, city ,country, attacker \
WHERE attack.id_attacker = attacker.id_attacker \
AND attacker.id_city = city.id_city \
AND city.id_country = country.id_country \
AND country.lib_country = c.lib_country \
GROUP BY lib_country) as Nb_attack_emmise \
FROM country c'

columns = ['Pays', 'Nb_attack_subie', 'Nb_attack_emmise']  
export_query_to_csv(sql, columns, 'NbrAttack_subie_emmise.csv')