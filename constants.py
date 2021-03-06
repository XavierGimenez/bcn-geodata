import base64

date_min = '201211'
date_max = '201304'

'''
boundaries found for Barcelona from shapefile
(2.05246984172867, 2.228097219280712, 41.32116390842041, 41.449787646748064)
API calls expect definition of half centesimal, so redefine boundaries:
(2.050, 2.220, 41.320, 41.450)
'''
geo_resolution = 0.005
westLng = 2.050
eastLng = 2.250
southLat = 41.320
northLat = 41.470

#vales obtaines after mapping geojson coordinates to pixels
pixelsWidth = 1000
pixelsHeight = 1143


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
