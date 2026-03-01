---
name: gis
version: "1.0.0"
category: engineering/gis
description: "Cross-application GIS skill — CRS reference, data formats, Blender/QGIS integration via digitalmodel.gis"
tags: [gis, geospatial, crs, geotiff, blender, qgis, wgs84, utm, geojson, shapefile]
platforms: [linux, windows, macos]
invocation: gis
capabilities: [input-generation, execution, output-parsing, failure-diagnosis, validation]
requires: []
see_also: [python-gis-ecosystem, qgis, gis-informed-workflow, google-earth-engine]
updated: "2026-02-24"
---

# GIS Skill — Integration Reference

Cross-application geospatial skill covering supported CRS, data formats, and
application integration steps for the `digitalmodel.gis` module (WRK-020).

---

## 1. Supported Coordinate Reference Systems

| EPSG | Name | Use case |
|------|------|----------|
| EPSG:4326 | WGS84 geographic | Default for GeoJSON, GPS, BSEE well data |
| EPSG:3857 | Web Mercator (Pseudo-Mercator) | Tile maps (Google Maps, OpenStreetMap) |
| EPSG:32601–32660 | UTM Zone 1N–60N | Northern hemisphere metre-accurate work |
| EPSG:32701–32760 | UTM Zone 1S–60S | Southern hemisphere metre-accurate work |
| EPSG:4269 | NAD83 | US onshore regulatory data |

Auto-detect UTM zone from longitude:

```python
from digitalmodel.gis.core.crs import get_utm_epsg
epsg = get_utm_epsg(longitude=-1.5, latitude=57.0)  # returns "EPSG:32630"
```

---

## 2. Supported Data Formats

| Format | Extensions | Handler | Notes |
|--------|-----------|---------|-------|
| GeoJSON | .geojson, .json | `io.geojson_handler.GeoJSONHandler` | No extra deps; RFC 7946 |
| KML / KMZ | .kml, .kmz | `io.kml_handler.KMLHandler` | Pure stdlib xml.etree |
| Shapefile | .shp + .dbf + .shx | `io.shapefile_handler.ShapefileHandler` | Requires geopandas/fiona |
| GeoTIFF | .tif, .tiff | `io.geotiff_handler.GeoTIFFHandler` | Requires rasterio |
| CSV + lat/lon | .csv | `layers.feature_layer.FeatureLayer` | Standard pandas read |
| WKT | embedded in .qgs / .csv | `core.geometry` | Used in QGIS project files |

---

## 3. Application Integration

### 3.1 QGIS

Generate a ready-to-open `.qgs` project file from a `WellLayer`:

```python
from digitalmodel.gis.integrations.qgis_export import QGISExporter
from digitalmodel.gis.layers.well_layer import WellLayer

layer = WellLayer.from_csv("wells.csv", lat_col="lat", lon_col="lon")
exporter = QGISExporter(layer)
exporter.generate_project("wells.qgs")          # open in QGIS 3.x
exporter.generate_well_qml("wells_style.qml")  # well marker style
```

Load a GeoTIFF bathymetry layer inside QGIS Processing Python console:

```python
iface.addRasterLayer("/path/to/bathymetry.tif", "Bathymetry")
```

### 3.2 Blender — Well Markers

Generate a Blender Python script that positions well cylinders in 3D:

```python
from digitalmodel.gis.integrations.blender_export import BlenderExporter
from digitalmodel.gis.layers.well_layer import WellLayer

layer = WellLayer.from_csv("wells.csv", lat_col="lat", lon_col="lon")
exporter = BlenderExporter(layer)
exporter.write_well_script("add_wells.py")
# In Blender: Text editor > Open add_wells.py > Run Script
```

### 3.3 Blender — Terrain / Bathymetry Mesh

Convert a GeoTIFF to an OBJ mesh that Blender can import directly:

```bash
python scripts/gis/geotiff-to-blender.py bathymetry.tif --output terrain.obj
# Optional: subsample to reduce vertex count
python scripts/gis/geotiff-to-blender.py bathymetry.tif --output terrain.obj --subsample 4
```

In Blender: **File > Import > Wavefront (.obj)** — select `terrain.obj`.

Scale defaults: 1 m = 0.001 Blender units (km scale). Override with
`--scale-xy` and `--scale-z`.

### 3.4 QGIS — Import Terrain as CSV Point Cloud

```bash
python scripts/gis/geotiff-to-blender.py bathymetry.tif --output points.csv
# QGIS: Layer > Add Layer > Add Delimited Text Layer > select points.csv
# Set X=x, Y=y, Z=z, CRS = source CRS of the GeoTIFF
```

### 3.5 worldenergydata.gis Module

```python
# Access BSEE well locations with CRS support
from worldenergydata.bsee import load_wells
wells_df = load_wells()  # lat/lon columns in WGS84
```

---

## 4. Bathymetry Sources

| Source | Resolution | Format | Notes |
|--------|-----------|--------|-------|
| GEBCO 2023 | 15 arc-sec (~500 m) | GeoTIFF | Global, free download |
| GEBCO via GEE | configurable | GeoTIFF export | See google-earth-engine skill |
| NOAA NCEI | 1 arc-sec (coastal US) | GeoTIFF | ETOPO series |

---

## 5. digitalmodel.gis Module Map

```
digitalmodel/gis/
  coordinates.py          — CoordinatePoint dataclass, batch transforms
  core/
    crs.py                — CRS definitions, get_utm_epsg()
    geometry.py           — GeoPoint, GeoBoundingBox, GeoPolygon
    spatial_query.py      — radius, bbox, polygon, nearest-N queries
    coordinate_transformer.py
  io/
    geojson_handler.py    — GeoJSON read/write
    kml_handler.py        — KML/KMZ read/write
    shapefile_handler.py  — Shapefile (optional geopandas)
    geotiff_handler.py    — GeoTIFF read/write/to_xyz (optional rasterio)
  layers/
    feature_layer.py      — FeatureLayer (pandas-backed GIS collection)
    well_layer.py         — WellLayer (well-specific subclass)
  integrations/
    blender_export.py     — Blender script generator for well markers
    qgis_export.py        — QGIS .qgs project + .qml style generator
    folium_maps.py        — Folium/Leaflet HTML maps
    google_earth_export.py— Styled KML for Google Earth
    plotly_maps.py        — Plotly mapbox scatter/dashboard
```

---

## 6. Failure Diagnosis

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError: rasterio not installed` | rasterio absent | `pip install rasterio` |
| `CRS mismatch in spatial join` | Layers in different CRS | `gdf.to_crs("EPSG:32631")` |
| OBJ mesh flipped Z in Blender | Depth values negative | Use `--scale-z -0.001` to invert |
| QGIS .qgs file not opening | QGIS version mismatch | Open via Layer > Add Vector Layer instead |
| Large OBJ causes Blender slowdown | Full-resolution raster | Use `--subsample 4` or higher |
