---
name: era5-download
description: Download ERA5 climate reanalysis data from the Copernicus Climate Data Store using cdsapi. Use this skill when users request ERA5 data, climate forcing data, meteorological variables, or need to download atmospheric/land surface data for ecosystem modeling, climate analysis, or model validation.
---

# ERA5 Download

## Overview

This skill enables downloading ERA5 reanalysis data from the Copernicus Climate Data Store (CDS) using the cdsapi Python package. ERA5 is a global atmospheric reanalysis dataset providing hourly estimates of atmospheric, land, and ocean climate variables from 1940 to present.

## Prerequisites

Before downloading ERA5 data, ensure:

1. **cdsapi is installed**: Add via `uv add cdsapi` or `pip install cdsapi`
2. **CDS credentials configured**: Either:
   - Configuration file `~/.cdsapirc` with:
     ```
     url: https://cds.climate.copernicus.eu/api
     key: <YOUR-PERSONAL-ACCESS-TOKEN>
     ```
   - Or environment variable: `COPERNICUS_API_KEY=<token>`
3. **License accepted**: User must accept dataset Terms of Use at https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels

## Quick Start

### Simple Download
For straightforward downloads with known variables:

```python
import cdsapi

client = cdsapi.Client()
result = client.retrieve(
    "reanalysis-era5-single-levels",
    {
        "product_type": "reanalysis",
        "variable": ["2m_temperature", "total_precipitation"],
        "year": "2023",
        "month": "01",
        "day": ["01", "02"],
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "area": [46, -123, 44, -121],  # [N, W, S, E]
        "format": "netcdf",
    },
)
result.download("output.nc")
```

### Using the Bundled Script
For more complex downloads or command-line usage, use `scripts/download_era5.py`:

```bash
# Download 2m temperature for January 2023
uv run python scripts/download_era5.py \
  -v 2m_temperature \
  -s 2023-01-01 -e 2023-01-31 \
  -o temperature_jan2023.nc

# Download multiple variables for a specific region
uv run python scripts/download_era5.py \
  -v 2m_temperature total_precipitation surface_pressure \
  -s 2023-01-01 -e 2023-01-02 \
  -a 46 -123 44 -121 \
  -o climate_data.nc

# Download 6-hourly data at pressure levels (3D atmosphere)
uv run python scripts/download_era5.py \
  -v temperature geopotential \
  -s 2023-01-01 -e 2023-01-01 \
  --hours 00:00 06:00 12:00 18:00 \
  --pressure-levels 1000 850 500 \
  -o upper_air.nc
```

## Variable Selection

### Finding Variables
When users request specific climate variables:

1. **Search the reference**: Use grep on `references/era5_variables.md`:
   ```bash
   grep -i "temperature" references/era5_variables.md
   grep -i "precipitation" references/era5_variables.md
   grep "soil_moisture" references/era5_variables.md
   ```

2. **Common categories**: The reference organizes variables by:
   - Atmospheric Variables (temperature, precipitation, wind, pressure, radiation)
   - Land Surface Variables (soil temperature/moisture, vegetation, snow, runoff)
   - Pressure Level Variables (3D atmospheric data)

3. **Ecosystem modeling use case**: For typical biogeochemical modeling (like EcoSIM), commonly needed variables are:
   - `2m_temperature` - Air temperature
   - `total_precipitation` - Precipitation
   - `surface_pressure` - Atmospheric pressure
   - `surface_solar_radiation_downwards` - Solar radiation
   - `10m_u_component_of_wind`, `10m_v_component_of_wind` - Wind
   - `2m_relative_humidity` or `2m_dewpoint_temperature` - Humidity
   - Soil layers: `soil_temperature_level_1`, `volumetric_soil_water_layer_1`, etc.

### Variable Name Format
ERA5 uses underscored names (e.g., `2m_temperature`, not `t2m` or `2m-temperature`).

## Spatial and Temporal Subsetting

### Geographic Area
Subset downloads to specific regions using bounding box `[north, west, south, east]` in degrees:
- Script: `--area 46 -123 44 -121`
- Direct API: `"area": [46, -123, 44, -121]`
- Omit for global data

### Temporal Selection
Control time range and resolution:
- **Date range**: Specify start/end dates (YYYY-MM-DD format)
- **Hours**: Subset to specific times (e.g., 6-hourly: `["00:00", "06:00", "12:00", "18:00"]`)
- **Default**: All 24 hours per day

### Best Practices
1. **Start small**: Test with 1-2 days before downloading years of data
2. **Geographic subsetting**: Always use `--area` when possible to reduce download size
3. **Temporal subsetting**: Use `--hours` for sub-daily data if hourly resolution isn't needed
4. **Batch large requests**: Break multi-year downloads into yearly or monthly chunks

## Datasets

### Single-Level (2D) Data
Dataset: `reanalysis-era5-single-levels`
- Surface and near-surface variables
- Integrated atmospheric columns
- Land surface conditions
- Use when variables don't require pressure levels

### Pressure-Level (3D) Data
Dataset: `reanalysis-era5-pressure-levels`
- Upper air meteorology (temperature, geopotential, winds)
- Requires `pressure_level` parameter (e.g., `[1000, 850, 500]` hPa)
- Use script flag: `--pressure-levels 1000 850 500`

## Output Formats

### NetCDF (Recommended)
- `format: "netcdf"` or `--format netcdf`
- Easier to work with in Python (xarray, netCDF4)
- Compatible with most modeling frameworks
- Self-describing with metadata

### GRIB
- `format: "grib"` or `--format grib`
- Standard meteorological format
- Requires specialized libraries (cfgrib, pygrib)

## Workflow Patterns

### Pattern 1: Climate Forcing for Models
When users need climate data to drive ecosystem/biogeochemical models:

1. Identify experimental site coordinates from metadata
2. Determine required variables for model forcing
3. Download ERA5 data for site location and time period
4. Convert to model-specific NetCDF format if needed

Example:
```python
# For EcoSIM forcing at experimental site
download_era5(
    variables=[
        "2m_temperature",
        "total_precipitation",
        "surface_pressure",
        "surface_solar_radiation_downwards",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
    ],
    start_date="2012-01-01",
    end_date="2022-12-31",
    area=[46.5, -122.5, 46.0, -122.0],  # Blodget site region
    output_file="ecosim_forcing_blodget.nc",
)
```

### Pattern 2: Multi-Site Meta-Analysis
When users have multiple experimental sites requiring climate data:

1. Read site metadata (e.g., from TSV/CSV with lat/lon)
2. Loop through sites, downloading data for each location
3. Use consistent temporal resolution and variables across sites
4. Save with systematic naming convention

### Pattern 3: Validation Data
When users need ERA5 data for model validation:

1. Download ERA5 estimates for validation variables (e.g., evaporation, runoff)
2. Match temporal and spatial resolution to model output
3. Ensure variables are comparable (same units, definitions)

## Troubleshooting

### License Not Accepted
Error: `403 Client Error: Forbidden ... required licences not accepted`

Solution: Visit dataset page and accept Terms of Use:
- Single-levels: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
- Pressure-levels: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels

### Authentication Issues
If cdsapi can't authenticate:
1. Check `~/.cdsapirc` exists with correct URL and key
2. Verify Personal Access Token from CDS profile
3. Check environment variable `COPERNICUS_API_KEY` if using that method

### Large Downloads Timing Out
For multi-year global datasets:
1. Break into smaller chunks (monthly/yearly)
2. Use geographic subsetting with `--area`
3. Reduce temporal resolution with `--hours`
4. Consider using ERA5-Land for land-only variables (higher resolution, smaller files)

### Wrong Variable Names
If variables aren't found:
1. Check spelling and underscores (e.g., `2m_temperature` not `2m-temperature`)
2. Verify variable exists in the chosen dataset (single-levels vs pressure-levels)
3. Consult `references/era5_variables.md` for correct names

## Resources

### scripts/download_era5.py
Flexible command-line tool for downloading ERA5 data with configurable parameters. Can be:
- Executed directly via command line
- Imported and used programmatically in Python
- Modified for project-specific needs

### references/era5_variables.md
Comprehensive reference of common ERA5 variables organized by category:
- Atmospheric variables (temperature, precipitation, wind, radiation)
- Land surface variables (soil, vegetation, snow, runoff)
- Pressure level variables (3D atmosphere)
- Common use cases for ecosystem modeling
- Variable naming conventions and tips

Load this reference when users need help identifying which ERA5 variables to download for their specific application.
