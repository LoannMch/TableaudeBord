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


sql = 'SELECT count(id_attack) as Nb_attack,co1.lib_country as \'Attaqué\',co2.lib_country as \'Attaquant\' \
FROM attack, attacker, city ci1, country co1, city ci2, country co2 \
WHERE attack.id_city = ci1.id_city \
AND  ci1.id_country =co1.id_country \
AND attack.id_attacker = attacker.id_attacker \
AND  attacker.id_city = ci2.id_city \
AND  ci2.id_country =co2.id_country \
GROUP BY co1.lib_country, co2.lib_country \
ORDER BY count(id_attack) DESC;'

columns = ['Nb_attack', 'Attaqué', 'Attaquant']  
export_query_to_csv(sql, columns, 'type_attack.csv')