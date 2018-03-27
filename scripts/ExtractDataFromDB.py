# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:19:54 2018

@author: Loann
"""

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
    tab = []
    nb_col = len(columns)
    for row in rows:
        col = []
        for i in range(nb_col):
            col.append(row[i])
        tab.append(col)
    df = pd.DataFrame(tab, columns=columns)
    df.to_csv('CSV_for_analyse/' + name_csv)


sql = 'SELECT lib_attacker, count(id_attack) \
FROM attacker, attack \
WHERE attack.id_attacker = attacker.id_attacker \
AND attack.id_city is null \
GROUP BY lib_attacker \
ORDER BY count(id_attack) DESC;'

columns = ['lib_attacker', 'Nb_attack']
export_query_to_csv(sql, columns, 'NbrAttack_Attacker.csv')

