'''
Created on 17/10/2013
@author: xavi

Signed degrees format (DDD.dddd)

A latitude or longitude with 8 decimal places pinpoints a location to within 1 millimeter,( 1/16 inch).

Precede South latitudes and West longitudes with a minus sign.
Latitudes range from -90 to 90. (horizontal)
Longitudes range from -180 to 180. (vertical)
41.25 and -120.9762
-31.96 and 115.84
90 and 0 (North Pole)
'''

#coordinates in the geojson is [lat, lng]
import json

#a simple port of simplify.js by Vladimir Agafonkin, a High-performance JavaScript polyline simplification library
from simplify import simplify

#set range of posible values for lattitude/longitude 
rangesLat = [-90, 90]
rangesLng = [-180, 180]
rangePixels = [0, 1000]

westLat = rangesLat[1]
eastLat = rangesLat[0]
southLng = rangesLng[1]
northLng = rangesLng[0]

#generic function to re-map a number from one range to another
def map(value, istart, istop, ostart, ostop):
    output = ostart + (ostop - ostart) * ((value - istart) / (istop - istart)) 
    return output

#functions to re-map a latitude value to pixels. ranges are boundary latitudes from our geojson and amount of pixels available 
def mapLatitude(value):
    return map(value, westLat, eastLat, rangePixels[0], rangePixels[1])
def mapLongitude(value):
    return map(value, southLng, northLng, rangePixels[0], rangePixels[1])

#map coordinates
def mapCoordinates(polygon):
    geometry = []
    for coordinate in polygon:
        # DO NOT round points! this will lead to bad accuracies when rendering (and a bunch of hours lost finding why)...
        #geometry.append([int(round(mapLatitude(coordinate[0]))), int(round(mapLongitude(coordinate[1])))])
        geometry.append([mapLatitude(coordinate[0]), mapLongitude(coordinate[1])])
    return geometry    
    
    '''for coordinate in polygon:
        geometry.append({"x":int(round(mapLatitude(coordinate[0]))), "y":int(round(mapLongitude(coordinate[1])))})
    
    #tolerance, from 0.1 to 5
    geometrySimplified = simplify(geometry, 0.1, True)
    
    #finally return points as lists of [lat, lng]
    geometry = []
    for point in geometrySimplified:
        geometry.append([point['x'], point['y']])
    return geometry
    '''
# look for min and max values. coordinates is an array of 2-value tuple
def searchBoundaries(coordinates):
    global westLat
    global eastLat
    global southLng
    global northLng
    for coordinate in coordinates:  
        if coordinate[0] < westLat:
            westLat = coordinate[0]      
        elif coordinate[0] > eastLat:            
            eastLat = coordinate[0]        
        if coordinate[1] < southLng:
            southLng = coordinate[1]
        elif coordinates[1] > northLng:
            northLng = coordinate[1]



data = json.loads(open('BCN-Illes.geojson').read())


#get from our geometry minimum and maximum values of latitude and longitude
for feature in data['features']:
    #inspect the type of geometry object
    if feature['geometry']['type'] == 'Polygon':
        polygon = feature['geometry']['coordinates'][0]
        searchBoundaries(polygon)
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polygon in feature['geometry']['coordinates'][0]:
            searchBoundaries(polygon)

print("boundaries:")
print(westLat, eastLat, southLng, northLng)

geometry = []
for feature in data['features']:
    #inspect the type of geometry object
    if feature['geometry']['type'] == 'Polygon':
        polygon = feature['geometry']['coordinates'][0]
        geometry.append(mapCoordinates(polygon))
    elif feature['geometry']['type'] == 'MultiPolygon':    
        for polygon in feature['geometry']['coordinates'][0]:
            geometry.append(mapCoordinates(polygon))    

totalPoints = 0    
for polygon in geometry:
    totalPoints += len(polygon)
print("total points ", totalPoints)


'''
TO IMPROVE AND ADD HERE: 
only two decimals are needed to display the city when mapping to pixels. The file BCN-Illes-datum.json
is readed by simplify_datum.py script, generating the file BCN-Illes-datum-rounded.json
This is the file readed in production nowadays (2013-10-15)
'''            
with open('BCN-Illes-datum.json', 'w') as outfile:
    json.dump({'geometry':geometry}, outfile)


#do the same with neighbourgods
data = json.loads(open('BCN_Barris.geojson').read())
geometry = []
for feature in data['features']:
    #inspect the type of geometry object
    if feature['geometry']['type'] == 'Polygon':
        polygon = feature['geometry']['coordinates'][0]
        geometry.append(mapCoordinates(polygon))
    elif feature['geometry']['type'] == 'MultiPolygon':    
        for polygon in feature['geometry']['coordinates'][0]:
            geometry.append(mapCoordinates(polygon))

with open('BCN-Barris-datum.json', 'w') as outfile:
    json.dump({'geometry':geometry}, outfile)
    
exit()
