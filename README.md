# Spatial Analysis Scripts – Bachelor's Thesis

This repository contains Python scripts developed as part of a bachelor's thesis named Geoinformation analysis of social segregation in relation to primary education (Hrabal 2025).

## Contents

### 1. `SWM.py`
This script generates a custom spatial weights matrix (`.swm`) for a set of polygon features (e.g., schools). The weights are computed based on a distance-decay function with defined inner and outer thresholds. The matrix can be used for spatial statistics, such as spatial lag computation.

**Key features:**
- Reads feature coordinates from a shapefile.
- Calculates distance-based weights (stepwise linear decay).
- Outputs a table-based spatial weights matrix and converts it to `.swm` using ArcPy.

### 2. `Jaccard.py`
This script calculates the Jaccard index for two sets of spatial features (e.g., hot spots of schools and SPO PNZ) across multiple buffer distances. It quantifies the degree of spatial overlap between the two datasets.

**Key features:**
- Generates buffers of increasing size for both shapefiles.
- Calculates area of intersection and union using ArcPy geometry tools.
- Outputs results (buffer distance, intersection area, union area, Jaccard index) to a `.csv` file.

### 3. `SpatialLag.py`
This script calculates the spatial lag (weighted average of neighboring values) for a given attribute column in a polygon shapefile, using a spatial weights matrix in `.swm` format (created in Script 1).

**Key features:**
- Loads data using GeoPandas.
- Computes spatial lag using PySAL's sparse matrix operations.
- Appends the computed spatial lag values to the original GeoDataFrame.
- Saves the result as a new shapefile.

## Requirements

- Python 3.x
- ArcPy (requires ArcGIS Desktop or ArcGIS Pro)
- GeoPandas
- PySAL (`libpysal`)
- NumPy
- CSV module (standard in Python)

## Notes

- All file paths have been anonymized for public release.
- Input shapefiles are assumed to be in a suitable projected coordinate system (e.g., JTSK or WGS84).
- These scripts were used in spatial analysis from 2017 to 2023, targeting educational and social inequality data.

## License

These scripts are provided for academic and educational purposes. Please cite appropriately if used in derivative work.

