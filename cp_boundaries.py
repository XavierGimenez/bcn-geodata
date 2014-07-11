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

#map coordinates
def mapCoordinates(polygon):
    geometry = []
    for coordinate in polygon:
        # DO NOT round points! this will lead to bad accuracies when rendering (and a bunch of hours lost finding why)...
        #geometry.append([int(round(mapLatitude(coordinate[0]))), int(round(mapLongitude(coordinate[1])))])
        geometry.append([ round(mapLatitude(coordinate[1]), 2), round(mapLongitude(coordinate[0]), 2) ])
    return geometry    

json_file = open("bcn-cp-boundaries.geojson")
data = json.load(json_file)
json_file.close()

cpBoundaries = {}

for feature in data['features']:
    geometry = []
    #inspect the type of geometry object
    if feature['geometry']['type'] == 'Polygon':
        polygon = feature['geometry']['coordinates'][0]
        geometry.append(mapCoordinates(polygon))
    elif feature['geometry']['type'] == 'MultiPolygon':    
        for polygon in feature['geometry']['coordinates'][0]:
            geometry.append(mapCoordinates(polygon))
    cpBoundaries[feature['properties']['COD_POSTAL']] = geometry

with open("customer-zip-codes/postalcodes_boundaries.json", 'w') as outfile:
    json.dump(cpBoundaries, outfile)

print("postal codes boundaries saved")