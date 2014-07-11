import constants

#generic function to re-map a number from one range to another
def map(value, istart, istop, ostart, ostop):
    output = ostart + (ostop - ostart) * ((value - istart) / (istop - istart)) 
    return output

#functions to re-map a latitude value to pixels. ranges are boundary latitudes from our geojson and amount of pixels available 
def mapLatitude(value):
    return map(value, constants.southLat, constants.northLat, 0, constants.pixelsHeight)
def mapLongitude(value):
    return map(value, constants.westLng, constants.eastLng, 0, constants.pixelsWidth)

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

#requests all the geo cells for the given week.
latitudes = frange(constants.southLat, constants.northLat, constants.geo_resolution)
longitudes = frange(constants.westLng, constants.eastLng, constants.geo_resolution)

latitudesMapped = []
longitudesMapped = []

for i in latitudes:    
    latitudesMapped.append(mapLatitude(i))
for i in longitudes:
    longitudesMapped.append(mapLongitude(i))
 
    
    
#he have the centers, now generate the left-bottom corner (used to be drawn in webgl) 
'''latitudesCorners = []
longitudesCorners = []
for i in latitudesMapped:
    latitudesCorners.append(i - (constants.geo_resolution/2))
for i in longitudesMapped:
    longitudesCorners.append(i - (constants.geo_resolution/2))
'''
print("latitudes ---")    
for i in latitudesCorners:
    print(i)
    
print("longitudes ---")
for i in longitudesCorners:
    print(i)
        
    