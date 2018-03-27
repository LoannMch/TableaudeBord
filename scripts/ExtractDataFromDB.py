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


sql = 'SELECT lib_country, COUNT(id_attack) AS Nb_attack \
FROM attack, organisation, country \
WHERE attack.id_organisation = organisation.id_organisation \
AND organisation.id_country = country.id_country \
GROUP BY lib_country \
ORDER BY COUNT(id_attack) DESC;'

columns = ['Pays', 'Nb_attack']
export_query_to_csv(sql, columns, 'NbrAttack_Pays_ZoneH.csv')
