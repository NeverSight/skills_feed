---
name: geopandas
description: Use when "GeoPandas", "geospatial", "GIS", "shapefile", "GeoJSON", or asking about "spatial analysis", "coordinate transformation", "spatial join", "choropleth map", "buffer analysis", "geographic data", "map visualization"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/geopandas -->

# GeoPandas Geospatial Data Analysis

Python library for geospatial vector data - extends pandas with spatial operations.

## When to Use

- Working with geographic/spatial data (shapefiles, GeoJSON, GeoPackage)
- Spatial analysis (buffer, intersection, spatial joins)
- Coordinate transformations and projections
- Creating choropleth maps
- Processing geographic boundaries, points, lines, polygons

## Quick Start

```python
import geopandas as gpd

# Read spatial data
gdf = gpd.read_file("data.geojson")

# Basic exploration
print(gdf.head())
print(gdf.crs)  # Coordinate Reference System
print(gdf.geometry.geom_type)

# Simple plot
gdf.plot()

# Reproject to different CRS
gdf_projected = gdf.to_crs("EPSG:3857")

# Calculate area (use projected CRS)
gdf_projected['area'] = gdf_projected.geometry.area

# Save to file
gdf.to_file("output.gpkg")
```

## Reading/Writing Data

```python
# Read various formats
gdf = gpd.read_file("data.shp")       # Shapefile
gdf = gpd.read_file("data.geojson")   # GeoJSON
gdf = gpd.read_file("data.gpkg")      # GeoPackage

# Read with spatial filter (faster for large files)
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# Write to file
gdf.to_file("output.gpkg")
gdf.to_file("output.geojson", driver="GeoJSON")

# PostGIS database
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
gdf = gpd.read_postgis("SELECT * FROM table", con=engine, geom_col='geom')
```

## Coordinate Reference Systems

```python
# Check CRS
print(gdf.crs)

# Set CRS (when metadata missing)
gdf = gdf.set_crs("EPSG:4326")

# Reproject (transforms coordinates)
gdf_projected = gdf.to_crs("EPSG:3857")  # Web Mercator
gdf_projected = gdf.to_crs("EPSG:32633")  # UTM zone 33N

# Common CRS codes:
# EPSG:4326 - WGS84 (lat/lon)
# EPSG:3857 - Web Mercator
# EPSG:326XX - UTM zones
```

## Geometric Operations

```python
# Buffer (expand/shrink geometries)
buffered = gdf.geometry.buffer(100)  # 100 units buffer

# Centroid
centroids = gdf.geometry.centroid

# Simplify (reduce vertices)
simplified = gdf.geometry.simplify(tolerance=5, preserve_topology=True)

# Convex hull
hull = gdf.geometry.convex_hull

# Boundary
boundary = gdf.geometry.boundary

# Area and length (use projected CRS!)
gdf['area'] = gdf.geometry.area
gdf['length'] = gdf.geometry.length
```

## Spatial Analysis

### Spatial Joins

```python
# Join based on spatial relationship
joined = gpd.sjoin(gdf1, gdf2, predicate='intersects')
joined = gpd.sjoin(gdf1, gdf2, predicate='within')
joined = gpd.sjoin(gdf1, gdf2, predicate='contains')

# Nearest neighbor join
nearest = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)
```

### Overlay Operations

```python
# Intersection
intersection = gpd.overlay(gdf1, gdf2, how='intersection')

# Union
union = gpd.overlay(gdf1, gdf2, how='union')

# Difference
difference = gpd.overlay(gdf1, gdf2, how='difference')
```

### Dissolve (Aggregate by Attribute)

```python
# Merge geometries by attribute
dissolved = gdf.dissolve(by='region', aggfunc='sum')
```

### Clip

```python
# Clip data to boundary
clipped = gpd.clip(gdf, boundary_gdf)
```

## Visualization

```python
import matplotlib.pyplot as plt

# Basic plot
gdf.plot()

# Choropleth map
gdf.plot(column='population', cmap='YlOrRd', legend=True)

# Multi-layer map
fig, ax = plt.subplots(figsize=(10, 10))
gdf1.plot(ax=ax, color='blue', alpha=0.5)
gdf2.plot(ax=ax, color='red', alpha=0.5)
plt.savefig('map.png', dpi=300, bbox_inches='tight')

# Interactive map (requires folium)
gdf.explore(column='population', legend=True)
```

## Common Workflows

### Spatial Join and Aggregate

```python
# Join points to polygons
points_in_polygons = gpd.sjoin(points_gdf, polygons_gdf, predicate='within')

# Aggregate by polygon
aggregated = points_in_polygons.groupby('index_right').agg({
    'value': 'sum',
    'count': 'size'
})

# Merge back to polygons
result = polygons_gdf.merge(aggregated, left_index=True, right_index=True)
```

### Buffer Analysis

```python
# Create buffers around points
gdf_projected = points_gdf.to_crs("EPSG:3857")  # Project first!
gdf_projected['buffer'] = gdf_projected.geometry.buffer(1000)  # 1km buffer
gdf_projected = gdf_projected.set_geometry('buffer')

# Find features within buffer
within_buffer = gpd.sjoin(other_gdf, gdf_projected, predicate='within')
```

## Best Practices

1. **Always check CRS** before spatial operations
2. **Use projected CRS** for area/distance calculations
3. **Match CRS** before spatial joins or overlays
4. **Validate geometries** with `.is_valid` before operations
5. **Use GeoPackage** format over Shapefile (modern, better)
6. **Use `.copy()`** when modifying geometry to avoid side effects
7. **Filter during read** with `bbox` for large files

## vs Alternatives

| Tool | Best For |
|------|----------|
| **GeoPandas** | Vector data analysis, spatial operations |
| Rasterio | Raster data (satellite imagery, DEMs) |
| Shapely | Low-level geometry operations |
| Folium | Interactive web maps |

## Resources

- Docs: <https://geopandas.org/>
- User Guide: <https://geopandas.org/en/stable/docs/user_guide.html>
- Gallery: <https://geopandas.org/en/stable/gallery/index.html>
