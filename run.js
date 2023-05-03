const fs = require('fs');
const path = require('path');

const TILE_FOLDER = "C:\\Users\\urus\\Desktop\\tilesDownload\\";
const MAP_URL = "https://geoportal.sedam.ro.gov.br/mosaicos/sentinel/072022/";

// Define a função que converte longitude em coordenada de tile x
const long2tile = function (lon, zoom) {
    return (Math.floor((lon + 180) / 360 * Math.pow(2, zoom)));
  }
    
  // Define a função que converte latitude em coordenada de tile y
  const lat2tile = function (lat, zoom) {
    return (Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom)));
  }
    
  
  // Chame a função com os limites da região, o zoom mínimo e máximo desejados
  const getTilesInBoundingBox  = function (bbox, minZoom, maxZoom) {
    if(!Array.isArray(bbox)) {
      return "Bounding Box must be informed. Type of ARRAY, example: [-63.80030,-9.02742,-63.21144,-8.66163]";
    }
    else if (!minZoom){
      return "Min Zoom must be informed.";
    }
    else if(!maxZoom){
      maxZoom = minZoom
    }
    // Crie uma matriz para armazenar os tiles
    const [west, south, east, north] = bbox;
  
    const tiles = [];
  
    // Percorra os níveis de zoom especificados
    for (let zoom = minZoom; zoom <= maxZoom; zoom++) {
      // Obtenha as coordenadas x e y do tile mínimo e máximo da região
      const minTileX = long2tile(west, zoom);
      const maxTileX = long2tile(east, zoom);
      const minTileY = lat2tile(north, zoom);
      const maxTileY = lat2tile(south, zoom);
  
      // Percorra os tiles x e y na região
      for (let x = minTileX; x <= maxTileX; x++) {
        for (let y = minTileY; y <= maxTileY; y++) {
          // Adicione o tile à matriz
          tiles.push({ x, y, z: zoom });
        }
      }
    }
    return tiles;
  }
     
const getTilesInCoordinate = function (bbox, minZoom, maxZoom, onFinish) {
  const tiles = getTilesInBoundingBox(bbox, minZoom, maxZoom)[0];
  console.log(tiles)
  const localLocation = `${TILE_FOLDER}/${tile.z}/${tile.x}/${tile.y}.png`;

  async function fetchTiles() {
    // Create directory for tiles
    // TODO: Batch to speed up
    for (const tile of tiles) {
      const folder = `${TILE_FOLDER}/${tile.z}/${tile.x}`;
      let dirInfo = await fs.promises.stat(folder).catch(() => null);
      if (!dirInfo || !dirInfo.isDirectory()) {
        await fs.promises.mkdir(folder, { recursive: true });
      }
    }
    // Download tiles in batches to avoid excessive promises in flight
    const BATCH_SIZE = 100;
    let batch = [];
    let uriLocal = undefined;
    for (const tile of tiles) {
      const fetchUrl = `${MAP_URL}/${tile.z}/${tile.x}/${tile.y}.png`;
      const tilePromise = new Promise(async (resolve, reject) => {
        const writer = fs.createWriteStream(localLocation);
        const response = await fetch(fetchUrl);
        response.body.pipe(writer);
        writer.on('finish', resolve);
        writer.on('error', reject);
      });

      // console.log(fetchUrl)
      uriLocal = localLocation;

      batch.push(tilePromise);
      if (batch.length >= BATCH_SIZE) {
        await Promise.all(batch);
        batch = [];
      }
    }
    await Promise.all(batch);
    onFinish(uriLocal);
  }

  fetchTiles();
};


getTilesInCoordinate([-63.80030,-9.02742,-63.21144,-8.66163], 7,10)