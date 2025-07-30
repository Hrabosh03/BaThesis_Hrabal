import geopandas as gpd
import libpysal
import numpy as np
import os

# --- Input paths ---
input_shapefile = r"<path_to_input_shapefile>.shp"           # Polygon layer with attribute data
weights_matrix_path = r"<path_to_weights_matrix>.swm"        # Spatial weights matrix file (.swm)
output_shapefile = r"<path_to_output_shapefile>.shp"         # Destination for output file

# --- Settings ---
value_column = "Index"   # Column containing the variable of interest

# Load input shapefile into GeoDataFrame
gdf = gpd.read_file(input_shapefile)
x = gdf[value_column].astype(float).values  # Convert column to NumPy array

# Load spatial weights matrix
f = libpysal.io.open(weights_matrix_path)
w = f.read()
f.close()
w.transform = "r"  # Row-standardization

# Calculate spatial lag (weighted average of neighboring values)
spatial_lag = w.sparse @ x
gdf["spatial_lag"] = spatial_lag

# Save the output shapefile (UTF-8 encoding)
if os.path.exists(output_shapefile):
    os.remove(output_shapefile)

gdf.to_file(output_shapefile, encoding="utf-8")
