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



print(mapLongitude(2.069), mapLatitude(41.3566))