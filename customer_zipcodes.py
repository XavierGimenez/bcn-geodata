import constants
import json
import requests
import time

'''
The access to the API services for each registered app will be free of charge for the Innova Challege contest. 
Anyway, there are certain limitations to requests for each app: 1000 requests per hour and 60 requests per second
'''
url = 'https://api.bbva.com/apidatos/zones/customer_zipcodes.json'
date_min = '201301'
date_max = '201301'
params = {'formatResponse':'json',
          #'date_min': date_min,
          #'date_max': date_max,
          'group_by':'week',
          'time_window':'1',
          'latitude':'40.420182',
          'longitude':'-3.70584',
          'zoom':'2',
          'by':'incomes',
          'category':'all',
          'order_by':'incomes'}
''''r = requests.get(url, params = params, headers=constants.headers)
data = r.json()
print(json.dumps(data))'''


#generate all the cells (coordinates are the cell's center)
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

date_ranges = [];
#date_ranges.append('201211')
#date_ranges.append('201212')
#date_ranges.append('201301')
#date_ranges.append('201302')
#date_ranges.append('201303')
#date_ranges.append('201304')
date_ranges.append('201305')
date_ranges.append('201306')


latitudes = []
longitudes = []
for longitude in frange(constants.westLng, constants.eastLng, constants.geo_resolution):
    longitudes.append(longitude)
for latitude in frange(constants.southLat, constants.northLat, constants.geo_resolution):
    latitudes.append(latitude)


#prepare the object that will hold the data for a given month
weeksData = {}

requestCounter = 0;

#asking for date_min=201211 and date_max=201304 results in 4 months, 23 weeks
for idmonth, month in enumerate(date_ranges[:-1]):
    #print("* * * * * * * month", month)
    #define the month to ask for
    params['date_min'] = month
    params['date_max'] = date_ranges[idmonth+1]
    #request for all cells for each month
    for idlng, longitude in enumerate(longitudes):
        for idlat, latitude in enumerate(latitudes):
            #wait until requesting a cell
            time.sleep(5)
            #define coordinate of the cell to ask for 
            params['longitude'] = longitude
            params['latitude'] = latitude
            #print("asking for ", longitude, latitude, "month:",month)
            #call to webservice
            r = requests.get(url, params = params, headers=constants.headers)
            response = r.json()
            requestCounter += 1
            print("request n ", idlng, idlat, requestCounter)
            #check if the result is OK
            if response['result']['code'] == 200:
                #print("ok")
                #loop for all the weeks of the month
                for week in response['data']['stats']:
                    #get sure we have an object to store the weeks' data.
                    if not week['date'] in weeksData:
                        weeksData[week['date']] = {}
                    #store data of the cell for the given week.
                    cellKey = '' + str(idlng) + '-' + str(idlat)  
                    weeksData[week['date']][cellKey] = week['zipcodes']
            else:
                print("code ", response['result']['code'], " for ", idlng, " ", idlat);

#right now we have for each week data from all the cells.Create file for each week
for week in weeksData:    
    with open(str(week) + '.txt', 'w') as outfile:
        json.dump(weeksData[week], outfile)
  
#postal_codes_bcn_city = range(8001, 8042)
