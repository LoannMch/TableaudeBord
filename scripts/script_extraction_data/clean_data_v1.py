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


def retrieve_List(name_list):
    """
    Entrée:
        name_list: String
    Sortie:
        the_List: List
    Récupération d'une liste à partir de la simpleWiki
    """
    the_list = list()
    if not (df_simpleWiki['text'][df_simpleWiki['title'] == name_list].empty):
        txt = df_simpleWiki['text'][df_simpleWiki['title'] == name_list].item()
        for val in re.finditer('\[\[[A-Z](\w| )+\]\]', txt):
            if val.group(0)[2:-2] not in the_list:
                the_list.append(val.group(0)[2:-2])
    return(the_list)


def retrieve_dictCity(countries):
    """
    Entrée:
        country: String
    Sortie:
        dictCity: dictionnaire
    Création d'un dictionnaire contenant la liste des villes les plus connus
    par pays
    """
    dictCity = {}
    for countrie in countries:
        listCity = retrieve_List('List of cities in ' + countrie)
        cities = []
        for xx in listCity[1:]:
            cities.append(xx.lower())
        dictCity[countrie] = cities
    return(dictCity)


def replace_line_break(text):
    """
    Entrée:
        text: string
    Sortie:
        text: string
    Enlève les sauts de ligne de la chaine de caractère
    """
    if re.search('\n', text):
        text = ' '.join(text.split('\n'))
    return(text)


def sent_clean(text):
    """
    Entrée:
        text: string
    Sortie:
        text_clean: string
    Enlève les characters innatendues
    + les city en fin de chaine de character
    """
    text = text.lower()
    text_clean = ''
    ii = 0
    ok = True
    while ii < len(text) and ok:
        if (text[ii].isalpha() is True or text[ii] == '-' or text[ii] == ' ' or
                text[ii] == '.'):
            text_clean += text[ii]
        else:
            ok = False
        ii += 1
    if len(text_clean) != 0:
        if text_clean[-1] == ' ':
            text_clean = text_clean[0:len(text_clean)-1]
    words = text_clean.split(" ")
    n = len(words)
    if words[n-1] == 'city':
        text_clean = ' '.join(words[0:n-1])
    return(text_clean)


def retrieve_country_only(text, countries):
    """
    Entrée:
        text: string, countries: list
    Sortie:
        text_clean: string
    Renvoie le pays s'il est en debut ou en fin de chaine de caractère
    """
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
    """
    Entrée:
        countrie: string
    Sortie:
        countrie: string
    Harmonise united states
    """
    listUs = ['u.s.a', 'u.s.', 'u.s', 'us', 'u.s.a.']
    if countrie in listUs:
        countrie = 'united states'
    return(countrie)


def states_us():
    """
    Entrée:
    Sortie:
        list_states: list
    Recupère la liste des états des états unis
    """
    req = requests.get('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    soup = bs4.BeautifulSoup(req.text, "lxml")
    tag_states = soup.find_all('area', attrs={'shape': 'poly'})
    list_states = []
    for tag_state in tag_states:
        list_states.append(tag_state['title'].lower())
    return(list_states)


def turn_into_country(text, states, cities):
    """
    Entrée:
        text: string + states: list + cities: dict
    Sortie:
        text: string
    Convertie une ville ou un état en pays
    """
    if text in states:
        return('united states')
    else:
        for kcountry in cities.keys():
            if text in cities[kcountry]:
                return(kcountry)
    return(text)


def clean_country(country, listCountriesLow, listStates, dictCities):
    """
    Entrée:
        country: string + listCountriesLow :list
        listStates: list + dictCities: dict
    Sorties:
        country: string / np.nan
    Nettoie la localisation récupérée sur wikipedia et la convertie en pays
    quand c'est possible sinon renvoie np.nan
    """
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
    """
    Entrée:
        industry: string
    Sorties:
        industry: string / np.nan
    Netoie le type d'industrie récupérée sur wikipedia
    si on a rien recupérée on attribue la valeur nan
    """
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
    """
        Entrée:
            text: string
        Sorties:
            text: string
        Supprime les caractères qui ne sont pas alphanumerique
        en fin et en debut de chaine de caractère
    """
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
