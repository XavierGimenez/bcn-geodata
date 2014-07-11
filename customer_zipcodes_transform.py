import constants
from haversine import haversine
import json
import requests
import time

'''
after querying all the available period with data (October'12 - April'13), data
goes from week 44 of 2012 to week 17 of 2013
The data will be stored as:
{
    "26-12": {
        "km": 100,
        "city" : {
            "km": 40,
            "incomes": 2100
            "coords": [{}, {}, {}]
        }
        "province": {
            "km": 20,
            "incomes": 3000
            "num_cards": 22
        }
        "other": {
            "km": 40,
            "incomes": 2000
            "num_cards": 1
        }
    }
}
'''

#list to generate the filesnames to read.
weeks2012 = range(44,53)
weeks2013 = range(1,18)
def yearize(week_number, year):
    return str(year) + (str(week_number) if week_number >= 10 else ("0" + str(week_number)))          
filenames = map(yearize, weeks2012, ["2012"] * len(weeks2012)) + map(yearize, weeks2013, ["2013"] * len(weeks2013)) 
print(filenames)

#list with the postal codes of bcn city
def postalCodize(n):
    return (str("0800") if n < 10 else str("080")) + str(n)
bcnPostalCodes = map(postalCodize, range(1,43))



#generate the array of lng/lat tuples
latitudes = []
longitudes = []
for longitude in constants.frange(constants.westLng, constants.eastLng, constants.geo_resolution):
    longitudes.append(longitude)
for latitude in constants.frange(constants.southLat, constants.northLat, constants.geo_resolution):
    latitudes.append(latitude)


#helper methods to classify postal codes
def isFromBCNCity(postal_code):
    return postal_code in bcnPostalCodes

def isFromBCNProvince(postal_code):
    return postal_code[:2] == "08"

def initCellData():
    cellData = {}
    cellData["k"] = 0
    cellData["i"] = 0
    cellData["c"] = {}
    cellData["c"]["k"] = 0
    cellData["c"]["i"] = 0
    cellData["c"]["l"] = []
    cellData["p"] = {}
    cellData["p"]["k"] = 0
    cellData["p"]["i"] = 0
    cellData["p"]["nl"] = 0
    cellData["o"] = {}
    cellData["o"]["k"] = 0
    cellData["o"]["i"] = 0
    cellData["o"]["nl"] = 0
    return cellData


for filename in filenames:     
    #obj holding the processed data
    weekDataOut = {}
    
    #read file with weekly data
    json_file = open("customer-zip-codes/" + filename + ".txt")
    weekData = json.load(json_file)
    json_file.close()
    
    #open files with the saved postal codes/coordinates
    json_file = open("customer-zip-codes/postalcodes_locations.json")
    postalCodesLocations = json.load(json_file)
    json_file.close()
    
    for idlng, longitude in enumerate(longitudes):
        for idlat, latitude in enumerate(latitudes):
            print(filename, idlng, idlat)
            #check if this week has data for this cell
            cellKey = str(idlng) + '-' + str(idlat)
            if cellKey in weekData:
                weekDataOut[cellKey] = initCellData()
                for postalCodeObj in weekData[cellKey]:        
                    #check if we already have a location for this postal code, otherwise query to google map API
                    if not postalCodeObj["label"] in postalCodesLocations:
                        #add some delay between each call
                        time.sleep(0.5)
                        #get a coordinate from the postal code, this can be accomplished by calling 
                        #google maps API, as follows: 
                        #http://maps.googleapis.com/maps/api/geocode/json?address=Barcelona&components=postal_code:08760&sensor=false
                        url = "http://maps.googleapis.com/maps/api/geocode/json?address=Spain&components=postal_code:" + postalCodeObj["label"] + "&sensor=false"
                        r = requests.get(url)
                        location = r.json()
                        coord = None if location["status"] != "OK" else location["results"][0]["geometry"]["location"]
                        #save the location, we will save all them in a json file
                        postalCodesLocations[postalCodeObj["label"]] = coord 
                    else:                    
                        coord = postalCodesLocations[postalCodeObj["label"]]
          
                    if coord is not None:
                        #get distance of the customer's postal code from this cell
                        distance = haversine(latitude, longitude, coord["lat"], coord["lng"])
        
                        #add distance to the total
                        weekDataOut[cellKey]["k"] += distance
                        weekDataOut[cellKey]["k"] = round(weekDataOut[cellKey]["k"], 2)
                        weekDataOut[cellKey]["i"] += postalCodeObj["incomes"]
                        weekDataOut[cellKey]["i"] = round(weekDataOut[cellKey]["i"], 2)                
                            
                        #evaluate origin of postal code and add data on the right origin
                        origin = "c" if isFromBCNCity(postalCodeObj['label']) else "p" if isFromBCNProvince(postalCodeObj['label']) else "o"                     
                        weekDataOut[cellKey][origin]["k"] += distance
                        weekDataOut[cellKey][origin]["k"] = round(weekDataOut[cellKey][origin]["k"], 2)
                        
                        weekDataOut[cellKey][origin]["i"] += postalCodeObj["incomes"]
                        weekDataOut[cellKey][origin]["i"] = round(weekDataOut[cellKey][origin]["i"], 2)
                            
                        #for city origins, save its coordinates (we will paint it), for the rest just count
                        if origin == "c":
                            weekDataOut[cellKey][origin]["l"].append(postalCodeObj['label'])
                        else:
                            weekDataOut[cellKey][origin]["nl"] += 1
    
    #looped through all the cells for this week, save it and udpate postalCode locations file
    with open("customer-zip-codes/" + filename + "_data.json", 'w') as outfile:
        json.dump(weekDataOut, outfile)
    with open("customer-zip-codes/postalcodes_locations.json", 'w') as outfile:
        json.dump(postalCodesLocations, outfile)
        

print("customer zipcodes transform done")
                   
