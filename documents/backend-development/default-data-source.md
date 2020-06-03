# Default data source

We are using default data source:

## OSM Data

OSM Data is taken in the format of PBF from https://download.geofabrik.de/

OSM Data that we uses consists of:

 - OSM Admin boundaries (geometries) and level
 - OSM Buildings (geometries)
 - OSM Roads (geometries)
 
For more information, refer to [Extracting and filtering OSM data](extracting-and-filtering-osm-data.md)

## Population

We use World Population data in the format of raster from https://www.worldpop.org/

We load the raster data to table like this:

```shell script
raster2pgsql -a -F -t 100x100 <filename.tif> public.world_pop > data.sql
```

Using psql, the data can be piped to the database like this:
In this example, we piped to `gis` database. Assuming that we use postgres credentials.

```shell script
cat data.sql | psql -d gis
```
