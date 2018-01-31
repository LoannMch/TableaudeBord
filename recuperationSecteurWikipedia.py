# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:17:11 2018

@author: Céline
"""
import requests
import bs4
#import re

list_entreprise = ['Louis_Vuitton', 'aaguysgusi', 'Airbus', 'Jackdaniels', 'Fnac']
req = requests.get('https://en.wikipedia.org/wiki/Airbus')
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

for entreprise in list_entreprise:
    req = requests.get('https://en.wikipedia.org/wiki/' + entreprise)
    data = req.text
    soup = bs4.BeautifulSoup(data, "lxml")
    ii = 0
    balises_b = soup.find_all('b')
    page_ok = True
    while ii < len(soup.find_all('b')) and page_ok:
        if balises_b[ii].get_text() == 'Wikipedia does not have an article with this exact name.':
            page_ok = False
            print("La page n'existe pas")
        else:
            ii += 1
    if page_ok:
        print(entreprise)
        infobox = soup.find('table', attrs={'class': 'infobox vcard'}).get_text()
        tab = infobox.split()
        for balise_th in soup.find_all('th', attrs={'style': "padding-right:0.5em;"}):
            if balise_th.get_text() == 'Headquarters':
                pays = balise_th.parent.find('td').get_text().split(', ')[-1]
        if tab.index('Industry'):
            type_Industry = tab[tab.index('Industry')+1]
        else:
            type_Industry = 'NonCommuniqué'
        print(pays)
        print(type_Industry)
        


