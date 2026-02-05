---
name: netcdf-metadata
description: Extract and analyze metadata from NetCDF files. Use this skill when working with NetCDF (.nc) or CDL (.cdl) files to extract variable information, dimensions, attributes, and data types to CSV format for documentation and analysis.
---

# NetCDF Metadata Extraction

## Overview

This skill provides tools for extracting metadata from NetCDF files into structured CSV format. Extract variable names, dimensions, shapes, data types, units, and all NetCDF attributes for documentation, analysis, and understanding NetCDF file contents.

## When to Use This Skill

Use this skill when:
- Working with NetCDF (.nc) or CDL (.cdl) files
- Needing to document NetCDF file contents
- Extracting variable lists and attributes to CSV
- Understanding NetCDF file structure before analysis
- Creating metadata catalogs for NetCDF datasets
- Comparing variables across multiple NetCDF files

## NetCDF File Formats

### Binary NetCDF (.nc files)

Binary format that xarray can read directly. Comes in two versions:
- **NetCDF3 (classic)**: Use `engine='scipy'` with xarray
- **NetCDF4/HDF5**: Use `engine='h5netcdf'` with xarray

### CDL Format (.nc.cdl files)

Text representation of NetCDF files. Must be converted to binary using `ncgen`:

```bash
ncgen -o output.nc input.nc.cdl
```

## Required Dependencies

Ensure the project has these dependencies installed:
- `xarray` - NetCDF file reading
- `scipy` - Backend for NetCDF3 classic format
- `h5netcdf` (optional) - Backend for NetCDF4/HDF5 format

Install with:
```bash
uv add xarray scipy h5netcdf
```

## Metadata Extraction

### Using the Extraction Script

The skill includes `scripts/extract_netcdf_metadata.py` which extracts all variable metadata to CSV.

**Usage:**

```bash
# Process all .nc files in a directory
uv run python scripts/extract_netcdf_metadata.py

# Process specific files
uv run python scripts/extract_netcdf_metadata.py file1.nc file2.nc
```

**Output:** Creates `.metadata.csv` files alongside each `.nc` file with the same basename.

**CSV Contents:**
- `variable_name` - NetCDF variable identifier
- `dimensions` - Dimension names (comma-separated)
- `shape` - Array shape as tuple
- `dtype` - Data type (float32, int8, etc.)
- `ndim` - Number of dimensions
- `size` - Total number of elements
- `long_name` - Human-readable description (if present)
- `units` - Measurement units (if present)
- Additional columns for any other NetCDF attributes (flags, FillValue, etc.)

### Manual Extraction with xarray

For custom metadata extraction or analysis:

```python
import xarray as xr

# Open NetCDF file (use engine='scipy' for NetCDF3)
ds = xr.open_dataset('file.nc', engine='scipy')

# Access metadata
print(ds)  # Overview of entire dataset
print(ds.dims)  # Dimensions
print(ds.data_vars)  # Data variables

# Access specific variable
var = ds['variable_name']
print(var.dims)  # Variable dimensions
print(var.shape)  # Variable shape
print(var.dtype)  # Data type
print(var.attrs)  # All attributes

# Access specific attributes
if 'long_name' in var.attrs:
    print(var.attrs['long_name'])
if 'units' in var.attrs:
    print(var.attrs['units'])

ds.close()
```

### Converting CDL to Binary NetCDF

When working with `.nc.cdl` files, convert them first:

```python
import subprocess
from pathlib import Path

cdl_file = Path("input.nc.cdl")
nc_file = cdl_file.with_suffix("").with_suffix(".nc")

subprocess.run(
    ["ncgen", "-o", str(nc_file), str(cdl_file)],
    check=True
)
```

Then read with xarray as normal.

## Common Patterns

### Document a Single NetCDF File

```bash
# Convert if CDL
ncgen -o data.nc data.nc.cdl

# Extract metadata
uv run python scripts/extract_netcdf_metadata.py data.nc
```

Result: `data.metadata.csv` created in the same directory.

### Batch Process Multiple Files

```bash
# Convert all CDL files in directory
for f in *.nc.cdl; do
    ncgen -o "${f%.cdl}" "$f"
done

# Extract metadata from all
uv run python scripts/extract_netcdf_metadata.py *.nc
```

### Compare Variables Across Files

Extract metadata from multiple files, then compare the CSV files to identify:
- Common variables across datasets
- Different variable names for the same concept
- Missing variables in specific files
- Attribute differences between datasets

## Troubleshooting

### "file signature not found" error

The NetCDF file is in classic format but xarray is using the wrong backend.

**Fix:** Use `engine='scipy'`:
```python
ds = xr.open_dataset(file, engine='scipy')
```

### "ncgen not found" error

The `ncgen` tool is not installed.

**Fix:** Install NetCDF tools:
```bash
# macOS
brew install netcdf

# Ubuntu/Debian
apt install netcdf-bin
```

### Missing backend libraries

xarray requires a backend to read NetCDF files.

**Fix:** Install scipy for NetCDF3:
```bash
uv add scipy
```

Or h5netcdf for NetCDF4:
```bash
uv add h5netcdf
```

## Script Reference

### scripts/extract_netcdf_metadata.py

Command-line tool that extracts variable metadata from NetCDF files to CSV format. Run directly without reading into context. The script:
- Accepts one or more NetCDF files as arguments
- Extracts all variable metadata (name, dimensions, shape, dtype, attributes)
- Writes CSV files with `.metadata.csv` extension alongside the original files
- Handles both NetCDF3 (classic) and NetCDF4 formats automatically
- Organizes CSV columns with standard fields first (variable_name, dimensions, shape, dtype, ndim, size, long_name, units)
