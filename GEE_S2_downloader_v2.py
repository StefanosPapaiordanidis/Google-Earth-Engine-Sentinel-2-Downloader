print('This script downloads Sentinel-2 2A images to a specified Google Drive folder.')
print('**MODULE REQUIREMENTS**')
print('earthengine-api')
print('geojson')
print('***********************')
print('## Access Authorization ##')
import geojson
import time
import ee
ee.Authenticate()
ee.Initialize()

def product_level():
    while True:
        plevel = str(input('Enter product level (2A or 1C): '))

        if plevel == '2A':
            Sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR')
            break
        elif plevel == '1C':
            Sentinel2 = ee.ImageCollection("COPERNICUS/S2")
            break
        else:
            print('Invalid choice, try again.')
    return Sentinel2

def get_coords():
    while True:  
        geojson_OR_coords = int(input('Type "1" if you are going to enter a GeoJSON path, or "2" if you are going to enter the points of the polygon manually: '))
        if geojson_OR_coords == 1:

            #GeoJSON to GEE Polygon
            geojson_path = str(input('Enter geojson path: '))
            with open(geojson_path) as f:
                gj = geojson.load(f)
            features = gj['features'][0]
            for f in range(len(features['geometry']['coordinates'][0][0])):
                if len(features['geometry']['coordinates'][0][0][f]) > 2:
                    features['geometry']['coordinates'][0][0][f] = features['geometry']['coordinates'][0][0][f][:2]
            coords = features['geometry']['coordinates'][0][0]
            break
        elif geojson_OR_coords == 2:
            print('The last point of the polygon does not need to be the same as the first.')
            npoints = int(input('How many points are you going to use for the polygon?: '))
            coords = []
            for p in range(npoints):
                print('Point ', p, ': ')
                temp_coord_long = float(input('Enter longtitude of point: '))
                temp_coord_lat = float(input('Enter latitude of point: '))
                
                coords.append([temp_coord_long, temp_coord_lat])
            break
        else:
            print('Invalid choice. Try again.')
    
    return coords

def get_dates():
    dateStart = str(input('Enter start date (yyyy-mm-dd): ')) #yyyy-mm-dd
    dateEnd = str(input('Enter end date (yyyy-mm-dd): '))     #yyyy-mm-dd
    dates = [dateStart, dateEnd]
    return dates

folder = str(input('Enter Google Drive folder name: '))

while True:
    print('Parameters: ')
    print(' 1. Product level')
    print(' 2. Polygon')
    print(' 3. Dates')
    print(' 4. Done setting parameters')
    
    choice = str(input('Type 1, 2, or 3 to set the coresponding parameters. Type 4 to continue.'))
    
    if choice == '1':
        Sentinel2 = product_level()
    elif choice == '2':
        boundary = ee.Geometry.Polygon(get_coords())
    elif choice == '3':
        dates = get_dates()
    elif choice == '4':
        col = Sentinel2.filterBounds(boundary).filterDate(dates[0], dates[1]).toList(10).getInfo()
        tiles = []
        for img in range(len(col)):
            tiles.append(col[img]['id'][-5:])
        if len(tiles) == 0:
            print('There are no images for the area you specified between ', dates[0], ' and ', dates[1])
        else:
            print('Possible tiles: ')
            for item in list(set(tiles)):
                print(item)
            tile = str(input('Enter Sentinel tile: '))
            break
    else:
        print('Invalid choice, try again.')
        

def clipFunction(image):
    return image.clip(boundary)
    
col = Sentinel2.filterBounds(boundary).filterDate(dates[0], dates[1]).filterMetadata('MGRS_TILE', 'equals', tile).map(clipFunction)

scale = 10                                          # Pixel size
Type = 'float'                                      # Data type of exported image (option: "float", "byte", "int", "double")
nimg = col.toList(600).size().getInfo()             # Number of images (automaticaly takes the lenght of the collection) **Caps at 600**
maxPixels = 1e10                                    # Max number of pixels to include in the image 
print('Images found: ', nimg)
#Image loop
print('Downloading...')
for i in range(nimg):
    img = ee.Image(col.toList(nimg).get(i))
    Id = img.id().getInfo()
    onlyDateId = img.get('PRODUCT_ID').getInfo().split('_')[2].split('T')[0]
        
    imgtype = {"float":img.toFloat(), 
               "byte":img.toByte(), 
               "int":img.toInt(),
               "double":img.toDouble()}
    
    task = ee.batch.Export.image.toDrive(imgtype[Type], 
                                         description=onlyDateId,
                                         folder=folder,
                                         fileNamePrefix=Id,
                                         region = boundary,
                                         scale = scale,
                                         maxPixels = maxPixels)
    task.start()
    task_id = task.id
    print(Id, ' = ', task.status()['state'])
    while task.status()['state'] != 'COMPLETED':
        time.sleep(2)
    print(Id, ' = ', task.status()['state'])
print('Finished!')
