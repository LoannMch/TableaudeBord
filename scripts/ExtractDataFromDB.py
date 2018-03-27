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


sql = 'SELECT x.month_date as mois, AVG(x.nb_attack) as nb_attack_moyen \
FROM (SELECT YEAR(attack.date_attack) AS year_date, MONTH(date_attack) AS month_date, count(id_attack) AS nb_attack \
		FROM attack \
		WHERE id_city is null \
		GROUP BY YEAR(date_attack), MONTH(date_attack)) x \
GROUP BY x.month_date \
ORDER BY x.month_date;'

columns = ['Month', 'Nb_attack_average']
export_query_to_csv(sql, columns, 'NbAttack_MonthAverage.csv')

