import constants
import json

#generic function to re-map a number from one range to another
def mapCoord(value, istart, istop, ostart, ostop):
    output = ostart + (ostop - ostart) * ((value - istart) / (istop - istart)) 
    return output

#functions to re-map a latitude value to pixels. ranges are boundary latitudes from our geojson and amount of pixels available 
def mapLatitude(value):
    return mapCoord(value, constants.southLat, constants.northLat, 0, constants.pixelsHeight)
def mapLongitude(value):
    return mapCoord(value, constants.westLng, constants.eastLng, 0, constants.pixelsWidth)

#list with the postal codes of bcn city
def postalCodize(n):
    return (str("0800") if n < 10 else str("080")) + str(n)
bcnPostalCodes = map(postalCodize, range(1,43))

#helper methods to classify postal codes
def isFromBCNCity(postal_code):
    return postal_code in bcnPostalCodes

 #read file with weekly data
json_file = open("customer-zip-codes/postalcodes_locations.json")
postalcodes = json.load(json_file)
json_file.close()

for postalcode in postalcodes:
    if isFromBCNCity(postalcode):
        postalcodes[postalcode]['x'] = round(mapLongitude(postalcodes[postalcode]['lng']), 2)
        postalcodes[postalcode]['y'] = round(mapLatitude(postalcodes[postalcode]['lat']), 2)

with open("customer-zip-codes/postalcodes_locations_xy.json", 'w') as outfile:
    json.dump(postalcodes, outfile)
