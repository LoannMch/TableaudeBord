import numpy as np
import requests as r
import bs4
import pandas as pd
import progressbar
from time import sleep
import logging as log


def call_api(api_url, to_parse_url) : 
	data = r.post(url = api_url, json = {"url" : to_parse_url, "wait" : 9, "expand" : 1, "timeout" : 90.0})
	data = data.text
	soup = bs4.BeautifulSoup(data, "lxml")
	data = soup.find_all('tr')
	return data


def extract_data(data) : 	
    data = np.array(data)
    pattern = '<td style="width: 14%;">Attack Type</td>'
    for i in range(len(data)) : 
        if pattern in str(data[i]): 
            return data[ i +1 : len(data)]

	#<td style="width: 34%;">Attacker</td>
	#<td style="width: 12%;">Attacker IP</td>
	#<td style="width: 12%;">Attacker Geo</td>
	#<td style="width: 12%;">Target Geo</td>
	#<td style="width: 14%;">Attack Type</td>


def delete_html(x) : 
    return x.text.split('\n')[2:][:-2]

def return_json(data) : 
	df = pd.DataFrame(np.array(data).reshape(len(data),5), columns = ['attacker', 'ip', 'attacker_country','target_country','attack_type'])

	df['attacker_town'] = df['attacker_country'].apply(lambda x : x.split(',')[0].replace(' ',''))
	df['target_town'] = df['target_country'].apply(lambda x : x.split(',')[0].replace(' ',''))
	df['attacker_country'] = df['attacker_country'].apply(lambda x : x.split(',')[1].replace(' ',''))
	df['target_country'] = df['target_country'].apply(lambda x : x.split(',')[1].replace(' ',''))
	
	return df.to_json(orient='index')


if __name__ == '__main__':

	api_url = 'http://localhost:8050/render.html'
	to_parse_url = "http://map.norsecorp.com/#/"

	iteration = 200


	bar = progressbar.ProgressBar(maxval=iteration, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	
	bar.start()

	for i in range(iteration):

		bar.update(i+1)
		try : 
			data = call_api(api_url, to_parse_url) 
			data = extract_data(data)
			data = list(map(delete_html, data))
			data = return_json(data) 
			print(data)
		except : 
			log.error('No Data Found. \n')

		


	bar.finish()

	