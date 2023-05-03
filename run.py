from xyz_tile_utils import getTilesInBoundingBox
from os import makedirs, getcwd, cpu_count
from os.path import exists, join
from requests import get
from concurrent.futures import ThreadPoolExecutor

TILE_FOLDER = getcwd()
MAP_URL = "https://geoportal.sedam.ro.gov.br/mosaicos/sentinel/072022/"
BATCH_SIZE = 100
batch = []


def download_tile(tile):
    folder = join(TILE_FOLDER, str(tile['z']), str(tile['x']))

    fetch_url = join(MAP_URL, str(tile['z']), str(tile['x']), f'{tile["y"]}.png')

    print(f'PASTA: {folder} || URL: {fetch_url}')

    if not exists(folder):
        makedirs(folder)

    r = get(url=fetch_url)

    out_file = join(folder, f'{tile["y"]}.png')

    if r.status_code == 200:
        with open(out_file, 'wb') as png:
            png.write(r.content)


def fetch_tiles(bbox, minZoom, maxZoom):
    tiles = getTilesInBoundingBox(bbox, minZoom, maxZoom)

    # Download tiles
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        for tile in tiles:
            executor.submit(download_tile, tile)

    print('OK')


if __name__ == '__main__':
    fetch_tiles([-63.80030, -9.02742, -63.21144, -8.66163], 7, 16)
