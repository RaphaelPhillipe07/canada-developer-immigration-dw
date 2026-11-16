# Map and province flag assets

## Geography
- Original: [Natural Earth Admin 1 subdivisions](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/), public domain.
- Retrieved as Canada FeatureCollection from [BenPortner/geojson-atlas](https://github.com/BenPortner/geojson-atlas/blob/main/geojson/natural_earth/countries/10m/CA.geojson), published under [CC0](https://github.com/BenPortner/geojson-atlas/blob/main/LICENSE.txt).
- Coordinates were simplified (Douglas–Peucker, 0.035 degrees) and rounded to 3 decimals for screen rendering. All 13 jurisdictions are retained. This is a small-scale visual guide, not a legal boundary product.
- Projection uses [D3 geoConicConformal](https://d3js.org/d3-geo/conic) with Canadian standard parallels 49/77 and central meridian 96°W.
- Local derivative: `src/canada-geography.ts`. Preparation recipe: `scripts/prepare-map-assets.mjs`.

## Flags
- All 13 SVG files in `public/flags` are real provincial/territorial flags, obtained from [Steven Skelton/flag-icon](https://github.com/stevenrskelton/flag-icon/tree/master/svg/ca).
- MIT license, Copyright (c) 2014 Steven Skelton. Full notice retained at `public/flags/LICENSE.txt`.
- Filename aliases use the project's province codes, preserving the original flag artwork.
- The assets are stored locally; visitor chart and map use requires no third-party image/CDN request.

## Canadian national flag
- public/flags/CA.svg: original vector from https://commons.wikimedia.org/wiki/File:Flag_of_Canada.svg (public domain; George F. G. Stanley / E Pluribus Anthony / Mzajac).
- Red and white artwork and 2:1 proportions preserved without recoloring.
- Geometry reference: https://www.canada.ca/en/canadian-heritage/services/flag-canada-description.html
