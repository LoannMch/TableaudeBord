# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:17:11 2018

@author: Céline

V0.1 : Cutting in function

"""
import requests
import bs4
import re
import numpy as np
import pandas as pd

data = pd.read_csv('myData21000.csv', sep=',',
                   error_bad_lines=False, encoding='ISO-8859-1')


def retrieve_infobox_wiki(company):
    missing_page = 'Wikipedia does not have an article with this exact name.'
    req = requests.get('https://en.wikipedia.org/wiki/' + company)
    soup = bs4.BeautifulSoup(req.text, "lxml")
    ii = 0
    tag_b = soup.find_all('b')
    page_ok = True
    while ii < len(soup.find_all('b')) and page_ok:
        if tag_b[ii].get_text() == missing_page:
            page_ok = False
        else:
            ii += 1
    if page_ok:
        infobox = soup.find('table', attrs={'class': 'infobox vcard'})
        return(infobox)


def retrieve_country(infobox):
    country = np.nan
    if infobox:
        for tag_th in infobox.find_all('th', attrs={"scope": "row"}):
            if tag_th.get_text() == 'Country':
                country = tag_th.parent.find('td').get_text()
            if tag_th.get_text() == 'Headquarters' and np.isnan(country):
                tag_country = tag_th.parent.find('td')
                country = tag_country.get_text().split(', ')[-1]
    return(country)


def retrieve_industry(infobox):
    type_Industry = np.nan
    if infobox:
        tab = infobox.get_text().split()
        if re.search('Industry ', ' '.join(tab)) is not None:
            type_Industry = tab[tab.index('Industry')+1]
    return(type_Industry)


df_infobox = pd.DataFrame(data[21000:41000]['company'].apply(
        retrieve_infobox_wiki))

for ii in range(21000, 21000+len(df_infobox)):
    if df_infobox['company'][ii]:
        data['retrieveIndustry'][ii] = retrieve_industry(
                df_infobox['company'][ii])
        data['retrieveCountry'][ii] = retrieve_country(
                df_infobox['company'][ii])

data.to_csv('myData41000.csv', sep=',', header=True, index=False)


print(data['retrieveCountry'].notnull().sum())
print(data['retrieveIndustry'].notnull().sum())


#17000 : 507 country et 444 Industry
#20000 : 595 country et 520 Industry
#20500 : 611 country & 535 Industry
#21000 : 623 country & 547 Indutry

###Objectif Vendredi : 
    #REMPLIR LA BASE DE DONNEE
    #AVANCER LE RAPPORT
    #FINIR ET METTRE LE CODE SUR GITHUB