import fs from 'node:fs/promises';
import {geoArea} from 'd3-geo';
const file='src/canada-geography.ts';
const text=await fs.readFile(file,'utf8');
const data=JSON.parse(text.split('export const canadaGeography = ')[1].replace(/ as const\s*$/,''));
for(const f of data.features){const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;for(const poly of polygons){if(geoArea({type:'Polygon',coordinates:poly})>2*Math.PI){poly.forEach(ring=>ring.reverse())}}}
await fs.writeFile(file,'// Natural Earth via GeoJSON Atlas, CC0. Simplified for screen rendering.\nexport const canadaGeography = '+JSON.stringify(data)+' as const\n');
let script=await fs.readFile('scripts/prepare-map-assets.mjs','utf8');
script=script.replace("import fs from 'node:fs/promises';","import fs from 'node:fs/promises';\nimport {geoArea} from 'd3-geo';");
script=script.replace("const collection=JSON.parse(await fs.readFile('public/maps/canada-original.tmp.geojson','utf8'));", "const collection=await (await fetch('https://raw.githubusercontent.com/BenPortner/geojson-atlas/main/geojson/natural_earth/countries/10m/CA.geojson')).json();");
script=script.replace('const data={type:', "for(const f of features){const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;for(const poly of polygons){if(geoArea({type:'Polygon',coordinates:poly})>2*Math.PI)poly.forEach(ring=>ring.reverse())}}\nconst data={type:");
await fs.writeFile('scripts/prepare-map-assets.mjs',script);
