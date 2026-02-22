---
name: xarray
description: N-dimensional labeled arrays and datasets in Python. Built on top of NumPy and Dask. It introduces labels in the form of dimensions, coordinates, and attributes on top of raw NumPy-like arrays, making data analysis in physical sciences more intuitive and less error-prone. Use for working with multi-dimensional scientific data, NetCDF/GRIB/Zarr files, climate/weather/oceanographic datasets, remote sensing, geospatial imaging, large out-of-memory datasets with Dask, and labeled array operations.
version: 2024.01
license: Apache-2.0
---

# Xarray - N-Dimensional Labeled Arrays

Xarray provides a pandas-like experience for multidimensional data. It is the core of the Pangeo ecosystem and is essential for working with NetCDF, GRIB, and Zarr formats.

## When to Use

- Working with multi-dimensional scientific data (Time, Lat, Lon, Level, Ensemble).
- Analyzing climate, weather, or oceanographic datasets (NetCDF files).
- Handling large datasets that don't fit in memory (via Dask integration).
- Performing complex broadcasting and alignment based on dimension names instead of axis indices.
- Storing metadata (units, descriptions) directly inside the data object.
- Remote sensing and geospatial imaging analysis.

## Reference Documentation

**Official docs**: https://docs.xarray.dev/  
**Tutorials**: https://tutorial.xarray.dev/  
**Search patterns**: `xr.DataArray`, `xr.Dataset`, `ds.sel`, `ds.groupby`, `ds.resample`, `xr.open_dataset`

## Core Principles

### DataArray vs Dataset

| Structure | Description | Analogy |
|-----------|-------------|---------|
| DataArray | A single labeled N-dimensional array. | Like a pandas.Series but N-D. |
| Dataset | A dict-like container of multiple DataArrays. | Like a pandas.DataFrame but N-D. |

### Key Concepts

- **Dimensions**: Names of the axes (e.g., x, y, time).
- **Coordinates**: Values associated with dimensions (e.g., actual timestamps or latitude values).
- **Attributes**: Arbitrary metadata (e.g., units='Kelvin', standard_name='air_temperature').

## Quick Reference

### Installation

```bash
pip install xarray netCDF4 dask zarr
```

### Standard Imports

```python
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### Basic Pattern - Creation

```python
import xarray as xr
import numpy as np

# Create a DataArray
data = np.random.rand(4, 3)
times = pd.date_range("2023-01-01", periods=4)
lons = [-120, -110, -100]

da = xr.DataArray(
    data, 
    coords={"time": times, "lon": lons}, 
    dims=("time", "lon"),
    name="temp",
    attrs={"units": "degC"}
)

# Convert to Dataset
ds = da.to_dataset()
print(ds)
```

## Critical Rules

### ✅ DO

- **Use Named Dimensions** - Always use `dim=('time', 'lat', 'lon')` instead of integer axes.
- **Select by Labels** - Use `.sel()` for coordinate values and `.isel()` for index integers.
- **Lazy Loading** - Use `chunks={}` in `open_dataset` to handle large files with Dask.
- **Keep Metadata** - Populate `.attrs` to ensure your data is self-describing.
- **Alignment** - Let Xarray handle broadcasting; it will automatically align data based on coordinate values.
- **Accessor power** - Use `.dt` for datetime and `.str` for string operations.

### ❌ DON'T

- **Use Integer Indexing** - Avoid `data[0, :, 5]` (unreadable and fragile). Use `.isel(time=0, lon=5)`.
- **Ignore the Encoding** - When saving to NetCDF, check `ds.encoding` for compression/scaling.
- **Manual Loops** - Don't loop over time steps; use `.groupby()` or `.resample()`.
- **Forget Dask** - For datasets larger than RAM, ensure Dask is installed and chunks are defined.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Positional indexing (What is axis 1? Lat or Lon?)
mean_val = ds.variable.mean(axis=1)

# ✅ GOOD: Named dimension reduction (Clear and robust)
mean_val = ds.variable.mean(dim='lat')

# ❌ BAD: Manual time slicing with list comprehensions
# subset = [ds.sel(time=t) for t in my_times if t > '2020-01-01']

# ✅ GOOD: Built-in slicing
subset = ds.sel(time=slice('2020-01-01', '2021-12-31'))

# ❌ BAD: Losing metadata during numpy conversion
raw_data = ds.temp.values # Now it's just a numpy array, units are gone!

# ✅ GOOD: Keep in Xarray as long as possible
processed = ds.temp * 10 # Units and coords are preserved
```

## Selection and Indexing

### sel vs isel

```python
# Select by coordinate values
subset = ds.sel(lat=45.0, lon=slice(-100, -80))

# Select by index (integer)
first_step = ds.isel(time=0)

# Nearest neighbor lookup
point = ds.sel(lat=42.1, lon=-71.2, method="nearest")

# Multi-dimensional selection
high_temp_days = ds.where(ds.temp > 30, drop=True)
```

## Computation and Math

### Broadcasting and Alignment

```python
# Xarray aligns automatically by coordinate names
da1 = xr.DataArray([1, 2], coords=[[1, 2]], dims=['x'])
da2 = xr.DataArray([1, 2, 3], coords=[[1, 2, 3]], dims=['y'])

# result is a 2x3 matrix
result = da1 + da2 

# Mathematical operations preserve coordinates
log_temp = np.log(ds.temp)
anomalies = ds.temp - ds.temp.mean(dim='time')
```

## GroupBy and Resampling

### Time Series and Spatial Aggregation

```python
# Monthly means
monthly = ds.resample(time="1MS").mean()

# Climatology (group by month regardless of year)
climatology = ds.groupby("time.month").mean()

# Calculate anomalies relative to climatology
anomalies = ds.groupby("time.month") - climatology

# Rolling window (Moving average)
rolling_mean = ds.rolling(time=7, center=True).mean()
```

## File I/O (NetCDF, Zarr)

### Reading and Writing

```python
# Open a single file
ds = xr.open_dataset("weather_data.nc")

# Open multiple files (MFDataset)
ds_all = xr.open_mfdataset("data/*.nc", combine="by_coords", chunks={'time': 100})

# Write to NetCDF
ds.to_netcdf("output.nc")

# Write to Zarr (Cloud optimized)
ds.to_zarr("data.zarr")
```

## Plotting

### High-level wrapping of Matplotlib

```python
# 1D plot
ds.temp.sel(lat=0, lon=0, method='nearest').plot()

# 2D map
ds.temp.isel(time=0).plot(cmap='RdBu_r', robust=True)

# Faceting (Subplots)
ds.temp.isel(time=slice(0, 4)).plot(col="time", col_wrap=2)
```

## Integration with pandas and NumPy

```python
# To Pandas
df = ds.to_dataframe()

# From Pandas
new_ds = xr.Dataset.from_dataframe(df)

# To NumPy (Lose coordinates)
arr = ds.temp.values

# Interoperability
# Xarray objects work in many SciPy/NumPy functions
from scipy.signal import detrend
detrended = xr.apply_ufunc(detrend, ds.temp, input_core_dims=[['time']], output_core_dims=[['time']])
```

## Advanced: Dask for Big Data

### Out-of-memory computation

```python
# Opening with chunks creates Dask arrays
ds = xr.open_dataset("huge_file.nc", chunks={'time': 500, 'lat': 100, 'lon': 100})

# Computation is now lazy
result = ds.temp.mean(dim='time') # Returns immediately

# Trigger computation
final_val = result.compute()
```

## Practical Workflows

### 1. Global Temperature Anomaly Workflow

```python
def calculate_temp_anomaly(filepath):
    """Calculate monthly anomalies from NetCDF data."""
    ds = xr.open_dataset(filepath)
    
    # 1. Compute climatology (mean for each month of the year)
    climatology = ds.temp.groupby("time.month").mean("time")
    
    # 2. Subtract climatology from original data
    anomalies = ds.temp.groupby("time.month") - climatology
    
    # 3. Global mean anomaly
    # Weighted by cos(lat) because grid cells get smaller at poles
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    anom_weighted = anomalies.weighted(weights)
    
    return anom_weighted.mean(("lat", "lon"))

# ts_anomaly = calculate_temp_anomaly("global_temps.nc")
```

### 2. Multi-Model Ensemble Analysis

```python
def analyze_ensemble(file_list):
    """Combine multiple model runs into a single dataset with a 'model' dimension."""
    datasets = [xr.open_dataset(f) for f in file_list]
    model_names = ["Model_A", "Model_B", "Model_C"]
    
    # Concatenate along a new dimension
    combined = xr.concat(datasets, dim=pd.Index(model_names, name="model"))
    
    # Calculate ensemble mean and spread
    ens_mean = combined.mean(dim="model")
    ens_std = combined.std(dim="model")
    
    return ens_mean, ens_std
```

### 3. Satellite Image Processing (NDVI)

```python
def calculate_ndvi(ds):
    """Calculate NDVI from Red and NIR bands in an Xarray Dataset."""
    # NDVI = (NIR - Red) / (NIR + Red)
    red = ds.sel(band='red')
    nir = ds.sel(band='nir')
    
    ndvi = (nir - red) / (nir + red)
    ndvi.attrs['long_name'] = "Normalized Difference Vegetation Index"
    
    return ndvi
```

## Performance Optimization

### Chunking Strategies

```python
# ❌ Problem: Small chunks lead to massive overhead
# ds = ds.chunk({'time': 1, 'lat': 1, 'lon': 1})

# ✅ Solution: Aim for 10MB - 100MB per chunk
ds = ds.chunk({'time': -1, 'lat': 100, 'lon': 100})
```

### Vectorization with apply_ufunc

```python
# Wrap a custom numpy function to work on Xarray objects efficiently
def my_complex_stat(x):
    return np.median(x) * np.std(x)

result = xr.apply_ufunc(
    my_complex_stat, 
    ds.temp,
    input_core_dims=[['time']], # The dimension to map the function over
    vectorize=True,
    dask="parallelized"
)
```

## Common Pitfalls and Solutions

### Coordinate Mismatch

```python
# ❌ Problem: DataArrays don't align due to floating point jitter in lat/lon
# ✅ Solution: Use .interp_like() or .reindex_like()
ds2_aligned = ds2.interp_like(ds1)
```

### Memory Leak with values

```python
# ❌ Problem: Calling .values on a huge Dask-backed array crashes the machine
# ✅ Solution: Use .compute() or subset first
subset_val = ds.temp.isel(time=0).values # This is safer
```

### Slicing issues (Start/End)

```python
# ❌ Problem: slice(10, 0) returns empty because order is wrong
# ✅ Solution: Check if your index is ascending or descending
# ds.sortby('lat').sel(lat=slice(-90, 90))
```

Xarray is the bridge between raw N-dimensional math and high-level data analysis. Its ability to handle labels and metadata makes scientific code self-documenting and significantly more reliable.
