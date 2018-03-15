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

data = pd.read_csv('FinalSource_Real Cases.csv', sep=',',
                   error_bad_lines=False, encoding='ISO-8859-1')


def extract_company(url):
    try:
        try:
            company = url.split('www.')[1]
        except:
            company = url.split('//')[1]
        company = company.split('.')[0]
        return company
    except:
        return np.nan

data['company'] = data['URL'].apply(extract_company)
data['retrieveCountry'] = pd.Series([np.nan]*212093)
data['retrieveIndustry'] = pd.Series([np.nan]*212093)




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
        if re.search('Industry ',' '.join(tab)) is not None:
            type_Industry = tab[tab.index('Industry')+1]
    return(type_Industry)


df_infobox = pd.DataFrame(data[17000:27000]['company'].apply(retrieve_infobox_wiki))

for ii in range(17000,17000+len(df_infobox)):
    if df_infobox['company'][ii]: 
        print(ii)
        data['retrieveIndustry'][ii] = retrieve_industry(df_infobox['company'][ii])
        data['retrieveCountry'][ii] = retrieve_country(df_infobox['company'][ii])
        
data.to_csv('myData27000.csv', sep=',', header=True, index=False)


#test_retrieve_Country = pd.DataFrame(data[0:12000]['company'].apply(retrieve_country))
#test_retrieve_Industry = pd.DataFrame(data[11000:12000]['company'].apply(retrieve_industry))

print(data['retrieveCountry'].notnull().sum())
print(data['retrieveIndustry'].notnull().sum())


#0:1000 --> 18pays & 15 industry 
#1000 :2000 --> 23 pays & 17 industry 
#2000:3000 -> 15 pays & 15 industry
#3000:4000 ->  33 pays & 29 industry
#4000:5000 -> 54 pays & 46 industry
#5000:6000 -> 17 pays & 17 industry
#6000:7000 -> 31 pays & 29 industry
#7000 : 8000 -> 38 pays et 32 industry
#8000:9000 -> 26 pays et 25 industry
#9000: 10000 -> 36 pays et 33 industry
#10000: 11000 -> 33 pays et 29 industry
#data['Country_retrieve'] = pd.DataFrame(data['company'].apply(retrieve_country))
#data['Industry_retrieve'] = pd.DataFrame(data['company'].apply(retrieve_industry))
###Objectif Vendredi : 
    #REMPLIR LA BASE DE DONNEE
    #AVANCER LE RAPPORT
    #FINIR ET METTRE LE CODE SUR GITHUB