import math
import os
import urllib.request
import asyncio

TILE_FOLDER = os.getcwd()
MAP_URL = "https://geoportal.sedam.ro.gov.br/mosaicos/sentinel/072022/"
BATCH_SIZE = 100
batch = []

def long2tile(lon, zoom):
    return int((lon + 180) / 360 * pow(2, zoom))

def lat2tile(lat, zoom):
    return int((1 - math.log(math.tan(lat * math.pi / 180) + 1 / math.cos(lat * math.pi / 180)) / math.pi) / 2 * pow(2, zoom))

def getTilesInBoundingBox(bbox, minZoom, maxZoom=None):
    if not isinstance(bbox, list):
        return "Bounding Box must be informed. Type of ARRAY, example: [-63.80030,-9.02742,-63.21144,-8.66163]"
    elif not minZoom:
        return "Min Zoom must be informed."
    elif not maxZoom:
        maxZoom = minZoom

    # Crie uma matriz para armazenar os tiles
    west, south, east, north = bbox
    tiles = []

    # Percorra os níveis de zoom especificados
    for zoom in range(minZoom, maxZoom+1):
        # Obtenha as coordenadas x e y do tile mínimo e máximo da região
        minTileX = long2tile(west, zoom)
        maxTileX = long2tile(east, zoom)
        minTileY = lat2tile(north, zoom)
        maxTileY = lat2tile(south, zoom)

        # Percorra os tiles x e y na região
        for x in range(minTileX, maxTileX+1):
            for y in range(minTileY, maxTileY+1):
                # Adicione o tile à matriz
                tiles.append({"x": x, "y": y, "z": zoom})

    return tiles

# print(getTilesInBoundingBox([-63.80030,-9.02742,-63.21144,-8.66163], 7,10))

def fetch_tiles(bbox, minZoom, maxZoom):
    tiles = getTilesInBoundingBox(bbox, minZoom, maxZoom)
    # Create directory for tiles
    for tile in tiles:
        folder = f"{TILE_FOLDER}\{tile['z']}\{tile['x']}"
        fetchUrl = f"{MAP_URL}/{tile['z']}/{tile['x']}/{tile['y']}.png"
        print(folder, fetchUrl)
        if not os.path.exists(folder):
            os.makedirs(folder)

   
        
    print('OK')

fetch_tiles([-63.80030,-9.02742,-63.21144,-8.66163], 7,12)