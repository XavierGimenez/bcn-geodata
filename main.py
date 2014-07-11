'''
Created on 07/10/2013

@author: xavi
'''

import json
import base64
import requests
from haversine import haversine

#print("haversine distance")
#print(haversine(41.387920, 2.169919, 41.393620, 2.009870))

#app_id:innova-challenge-big-data-viz
#app_key:061eb41cd6f662a0d607f04fdd1b3e7989de42a6
headers = {"Authorization":base64.b64encode("innova-challenge-big-data-viz:061eb41cd6f662a0d607f04fdd1b3e7989de42a6")}

'''
#call of commercial category information
url = 'https://api.bbva.com/apidatos/info/merchants_categories.json'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
params = {'formatResponse':'json'}
r = requests.get(url, params = params, headers=headers)
print(json.dumps(r.json()))
'''


#call example:
#https://api.bbva.com/apidatos/zones/customer_zipcodes.json?date_min=201301&date_max=201301&group_by=month&time_window=1&latitude=40.420182&longitude=-3.70584&zoom=2&category=es_fashion&by=incomes
'''
url = 'https://api.bbva.com/apidatos/zones/customer_zipcodes.json'
params = {'formatResponse':'json',
          'date_min':'201212',
          'date_max':'201301',
          'group_by':'week',
          'time_window':'1',
          'latitude':'40.420182',
          'longitude':'-3.70584',
          'zoom':'2',
          'by':'incomes',
          'category':'all',
          'order_by':'incomes'}
r = requests.get(url, params = params, headers=headers)
print(json.dumps(r.json()))
data = r.json()
'''

'''
#Consumption patterns
url = 'https://api.bbva.com/apidatos/zones/consumption_pattern.json'
params = {'date_min':'20121101',
          'date_max':'20130401',
          'group_by':'month',
          'latitude':'40.420182',
          'longitude':'-3.70584',
          'zoom':'2',
          'category':'all'}
r = requests.get(url, params = params, headers=headers)
data = r.json()
print(json.dumps(data))
'''


'''
#clients cube
url = 'https://api.bbva.com/apidatos/zones/cards_cube.json'
params = {'date_min':'201301',
          'date_max':'201302',
          'group_by':'week',
          'latitude':'40.420182',
          'longitude':'-3.70584',
          'zoom':'2'
          }
r = requests.get(url, params = params, headers=headers)
data = r.json()
print(json.dumps(data))
'''

print("end of program")


#