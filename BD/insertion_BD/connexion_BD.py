# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 13:39:37 2018

@author: Loann
"""

import pyodbc

# LAPTOP-4H4QSG7A\SQLEXPRESS
con = pyodbc.connect("Driver={SQL Server};"
                     "Server=LAPTOP-4H4QSG7A\SQLEXPRESS;"
                     "Database=master;"
                     "Trusted_Connection=yes;")

cursor = con.cursor()
cursor.execute('SELECT * FROM country')


for row in cursor:
    # print(row)
    print('row = %r' % (row,))
