# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 10:47:07 2018

@author: Celine
V0 : create function retrieve_List, retrieve_dictCity, replace_line_break,
                     sent2clean, retrieve_country_only, turn_into_country,
                     states_us, standardize_us, clean_country, clean_industry
V1 : create function clean_column

"""
import pandas as pd
import re
import bs4
import requests
import numpy as np

data = pd.read_csv('DataCountryClean.csv', sep=',',
                   error_bad_lines=False, encoding='ISO-8859-1')

df_simpleWiki = pd.DataFrame.from_csv('simplewiki.csv', encoding='utf-8')


def retrieve_List(nameList):
    laList = list()
    if not (df_simpleWiki['text'][df_simpleWiki['title'] == nameList].empty):
        text = df_simpleWiki['text'][df_simpleWiki['title'] == nameList].item()
        for val in re.finditer('\[\[[A-Z](\w| )+\]\]', text):
            if val.group(0)[2:-2] not in laList:
                laList.append(val.group(0)[2:-2])
    return(laList)


def retrieve_dictCity(countries):
    dictCity = {}
    for countrie in countries:
        listCity = retrieve_List('List of cities in ' + countrie)
        cities = []
        for xx in listCity[1:]:
            cities.append(xx.lower())
        dictCity[countrie] = cities
    return(dictCity)


def replace_line_break(text):
    if re.search('\n', text):
        text = ' '.join(text.split('\n'))
    return(text)


def sent_clean(sent):
    sent = sent.lower()
    sentClean = ''
    ii = 0
    ok = True
    while ii < len(sent) and ok:
        if (sent[ii].isalpha() is True or sent[ii] == '-' or sent[ii] == ' ' or
                sent[ii] == '.'):
            sentClean += sent[ii]
        else:
            ok = False
        ii += 1
    if len(sentClean) != 0:
        if sentClean[-1] == ' ':
            sentClean = sentClean[0:len(sentClean)-1]
    words = sentClean.split(" ")
    n = len(words)
    if words[n-1] == 'city':
        sentClean = ' '.join(words[0:n-1])
    return(sentClean)


def retrieve_country_only(text, countries):
    world = text.split(" ")
    n = len(world)
    test1 = world[n-1]
    test2 = world[0]
    for ii in range(1, 4):
        if test1 in countries:
            return(test1.lower())
        elif test2 in countries:
            return(test2.lower())
        test1 = ' '.join(world[n-1-ii:n])
        test2 = ' '.join(world[0:ii])
    return(text.lower())


def standardize_us(countrie):
    listUs = ['u.s.a', 'u.s.', 'u.s', 'us', 'u.s.a.']
    if countrie in listUs:
        countrie = 'united states'
    return(countrie)


def states_us():
    req = requests.get('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    soup = bs4.BeautifulSoup(req.text, "lxml")
    tag_states = soup.find_all('area', attrs={'shape': 'poly'})
    list_states = []
    for tag_state in tag_states:
        list_states.append(tag_state['title'].lower())
    return(list_states)


def turn_into_country(text, states, cities):
    if text in states:
        return('united states')
    else:
        for kcountry in cities.keys():
            if text in cities[kcountry]:
                return(kcountry)
    return(text)


def clean_country(country, listCountriesLow, listStates, dictCities):
    country = str(country).lower()
    country = replace_line_break(country)
    country = retrieve_country_only(country, listCountriesLow)
    country = sent_clean(country)
    country = standardize_us(country)
    country = turn_into_country(country, listStates, dictCities)
    if country not in listCountriesLow:
        country = np.nan
    return(country)


def clean_industry(industry):
    industry = str(industry).lower()
    if len(industry) > 0:
        while not industry[-1].isalpha():
            if len(industry)-1 > 0:
                industry = industry[0:len(industry)-1]
            else:
                industry = 'nan'
    if industry == 'nan':
        industry = np.nan
    return(industry)


def clean_column(text):
    text = str(text).lower()
    if len(text) > 0:
        while not(text[-1].isalpha() or text[-1].isnumeric()):
            if len(text)-1 > 0:
                text = text[0:len(text)-1]
            else:
                return('')
        while not(text[0].isalpha() or text[0].isnumeric()):
            if len(text)-1 > 0:
                text = text[1:len(text)]
            else:
                return('')
    return(text)

listCountries = sorted(retrieve_List('List of countries'))
listCountriesLow = [countrie.lower() for countrie in listCountries]
listStates = states_us()
dictCities = retrieve_dictCity(listCountries)


data['Country'] = data['Country'].apply(clean_country,
                            args=(listCountriesLow, listStates, dictCities))

data['retrieveIndustry'] = data['retrieveIndustry'].apply(clean_industry)

listColumns = list(data.columns.values)

for column in listColumns:
    data[column] = data[column].apply(clean_column)


data.to_csv('DataColumnsClean.csv', sep=',', header=True, index=False)
