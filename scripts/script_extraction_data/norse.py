import numpy as np
import requests as r
import bs4
import pandas as pd
import logging as log
import json
import datetime
import tqdm
import os
import uuid


def call_api(api_url, to_parse_url):
    """
        Entrée:
            api_url: url de l'api
            to_parse_url: url du site web norse
        Sorties:
            data: html contenant les données des cyberattaques
    """
    data = r.post(url=api_url, json={"url": to_parse_url, "wait": 10,
                                     "expand": 1, "timeout": 90.0})
    data = data.text
    soup = bs4.BeautifulSoup(data, "lxml")
    data = soup.find_all('tr')
    return data


def extract_data(data):
    """
        Entrée:
            data: html
        Sorties:
            data: html filtré
        Filtre le html, sélectionne les cyberattaques et retire la mise en forme
    """
    data = np.array(data)
    pattern = '<td style="width: 14%;">Attack Type</td>'
    for i in range(len(data)):
        if pattern in str(data[i]):
            return data[i + 1: len(data)]


def delete_html(x):
    """
        Entrée:
            x: html
        Sorties:
            x: html mis en forme
        Mise en forme du html
    """
    return x.text.split('\n')[2:][:-2]


def return_dic(data):
    """
        Entrée:
            data: objet pandas dataframe
        Sorties:
            records: dictionnaire orienté clé - valeur contenant les données
    """
    df = pd.DataFrame(np.array(data).reshape(len(data), 5),
                      columns=['attacker', 'ip', 'attacker_country',
                               'target_country', 'attack_type'])
    df['attacker_town'] = df['attacker_country'].apply(lambda x: x.split(',')[0].replace(' ', ''))
    df['target_town'] = df['target_country'].apply(lambda x: x.split(',')[0].replace(' ', ''))
    df['attacker_country'] = df['attacker_country'].apply(lambda x: x.split(',')[1].replace(' ', ''))
    df['target_country'] = df['target_country'].apply(lambda x: x.split(',')[1].replace(' ', ''))
    df['date'] = datetime.datetime.now().isoformat()
    return df.to_dict('records')


def write_json(data, cwd):
    """
        Entrée:
            data: dictionnaire orienté clé valeur
            cwd: current working directory
        procédures qui écrit json

    """
    # You must create a repertory norse_json
    with open('{}/norse_json/{}.json'.format(cwd, uuid.uuid4()), 'w') as outfile:
        outfile.write(json.dumps(data))


if __name__ == '__main__':
    # To Do - Run API splash with docker and bash command :
        # docker run -p 8050:8050 scrapinghub/splash
    api_url = 'http://localhost:8050/render.html'
    to_parse_url = "http://map.norsecorp.com/#/"
    cwd = os.getcwd()
    iteration = 10000
    nb_attack_extracted = 0
    attack_per_json = 0
    res = []
    counter = 0

    for ii in tqdm.trange(iteration):
        counter += 1
        try:
            data = call_api(api_url, to_parse_url)
            data = extract_data(data)
            data = list(map(delete_html, data))
            data = return_dic(data)
            nb_attack_extracted += len(data)
            res = res + data
            if counter >= 1000:
                write_json(res, cwd)
                print('Attacks analysed since the begining : {} \n.'.format(nb_attack_extracted))
                res = []
                counter = 0
        except:
            log.info('No Data Found. \n')
    if len(res) > 0:
        write_json(res, cwd)
        print('Attacks analysed since the begining : {}. \n'.format(nb_attack_extracted))
        print('Process terminated, {} attacks analysed. \n'.format(nb_attack_extracted))
