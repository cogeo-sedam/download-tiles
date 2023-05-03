from math import log, tan, pi, cos, pow


def long2tile(lon, zoom):
    return int((lon + 180) / 360 * pow(2, zoom))


def lat2tile(lat, zoom):
    return int(
        (1 - log(tan(lat * pi / 180) + 1 / cos(lat * pi / 180)) / pi) / 2 * pow(2, zoom))


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
    for zoom in range(minZoom, maxZoom + 1):
        # Obtenha as coordenadas x e y do tile mínimo e máximo da região
        minTileX = long2tile(west, zoom)
        maxTileX = long2tile(east, zoom)
        minTileY = lat2tile(north, zoom)
        maxTileY = lat2tile(south, zoom)

        # Percorra os tiles x e y na região
        for x in range(minTileX, maxTileX + 1):
            for y in range(minTileY, maxTileY + 1):
                # Adicione o tile à matriz
                tiles.append({"x": x, "y": y, "z": zoom})

    return tiles
