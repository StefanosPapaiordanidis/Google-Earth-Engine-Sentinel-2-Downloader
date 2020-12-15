# Google-Earth-Engine-Sentinel-2-Downloader
This script downloads Sentinel-2 images from Google Earth Engine to a specified Google Drive folder

Requirements:
- A Google account with Google Earth Engine Access (signup.earthengine.google.com)
- Python 3.7.6 
- earthengine-api (https://pypi.org/project/earthengine-api/)
- geojson (https://pypi.org/project/geojson/)

How to run:
- open a command line or Anaconda prompt and type "python /path/to/GEE_S2_downloader.py"

Features:
- You can select from Sentinel-2 product level 1C and 2A
- You can select the region you want either with a GeoJSON file, or you can enter the point latitude and logtitude manually 
- You select the time range of the images
- You select the Sentinel-2 specific tile
