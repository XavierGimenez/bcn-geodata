import json



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

json_file = open("temp/BCN-Illes-datum.json")
data = json.load(json_file)
json_file.close()


for polygon in data["geometry"]:
    for coordinate in polygon:
        coordinate[0] = round(coordinate[0], 2)
        coordinate[1] = round(coordinate[1], 2)

with open("temp/BCN-Illes-datum-rounded.json", 'w') as outfile:
        json.dump(data, outfile)