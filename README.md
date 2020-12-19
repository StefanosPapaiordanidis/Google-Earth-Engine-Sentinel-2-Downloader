# Google-Earth-Engine-Sentinel-2-Downloader
This script downloads Sentinel-2 images from Google Earth Engine to a specified Google Drive folder.
Each image is a .tif file named after the image product-id with all Sentinel-2 bands, clipped with a user-specified polygon. 

Requirements:
- A Google account with Google Earth Engine Access (https://signup.earthengine.google.com)
- Python 3.7.6 (maybe it works on later versions, haven't tried it) 
- earthengine-api (https://pypi.org/project/earthengine-api/)
- geojson (https://pypi.org/project/geojson/)

How to run:
- Create a folder in Google Drive. This is where the images will be saved
- Open a command line or Anaconda prompt and type: python /path/to/script/GEE_S2_downloader.py

Features:
- You can select from Sentinel-2 product level 1C and 2A
- You can select the region you want either with a GeoJSON file, or you can enter the point latitude and logtitude manually 
- You select the time range of the images
- You select the Sentinel-2 specific tile
