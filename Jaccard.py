import arcpy
import csv
import os

# Paths to input shapefiles (replace with actual relative or project paths)
shapefile_a = r"<path_to_first_layer>.shp"  
shapefile_b = r"<path_to_second_layer>.shp"  

# Path to output CSV file
output_csv = r"<output_directory>\Jaccard_results.csv"

# List of buffer distances (in meters) to test the spatial overlap
buffer_distances = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]

# Storage for results (headers)
results = [("buffer_dist", "inter_area", "union_area", "jaccard")]

for dist in buffer_distances:
    # Create buffers for both layers
    buf_a = arcpy.analysis.Buffer(shapefile_a, "in_memory/buf_a", f"{dist} Meters")
    buf_b = arcpy.analysis.Buffer(shapefile_b, "in_memory/buf_b", f"{dist} Meters")

    # Perform spatial intersection and union
    inter = arcpy.analysis.Intersect([buf_a, buf_b], "in_memory/inter")
    union = arcpy.analysis.Union([buf_a, buf_b], "in_memory/union")

    # Calculate area of intersection and union
    inter_area = sum(row[0] for row in arcpy.da.SearchCursor(inter, ["SHAPE@AREA"]))
    union_area = sum(row[0] for row in arcpy.da.SearchCursor(union, ["SHAPE@AREA"]))


    # Compute Jaccard index
    jaccard = inter_area / union_area if union_area != 0 else 0

    results.append((dist, inter_area, union_area, jaccard))

    # Clean up in-memory workspace
    arcpy.management.Delete("in_memory/buf_a")
    arcpy.management.Delete("in_memory/buf_b")
    arcpy.management.Delete("in_memory/inter")
    arcpy.management.Delete("in_memory/union")

# Save results to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(results)
