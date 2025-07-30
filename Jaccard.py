import arcpy
import csv
import os

# Cesty ke vstupním shapefilům
shapefile_a = r"C:\Skola\BP\vizualizace\skoly2017_Jaccard.shp"
shapefile_b = r"C:\Skola\BP\vizualizace\spopnz2017_Jaccard.shp"

# Cesta k výstupnímu CSV souboru
output_csv = r"C:\Skola\BP\data_analyza\Jaccard\Jaccard2017_results_1.csv"

# Seznam bufferových vzdáleností v metrech
buffer_distances = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]

# Seznam pro ukládání výsledků
results = [("buffer_dist", "inter_area", "union_area", "jaccard")]


for dist in buffer_distances:

    # Creating buffers
    buf_a = arcpy.analysis.Buffer(shapefile_a, "in_memory/buf_a", f"{dist} Meters")
    buf_b = arcpy.analysis.Buffer(shapefile_b, "in_memory/buf_b", f"{dist} Meters")

    # Intersect and Union
    inter = arcpy.analysis.Intersect([buf_a, buf_b], "in_memory/inter")
    union = arcpy.analysis.Union([buf_a, buf_b], "in_memory/union")

    # Calculating sum
    inter_area = sum(row[0] for row in arcpy.da.SearchCursor(inter, ["SHAPE@AREA"]))
    union_area = sum(row[0] for row in arcpy.da.SearchCursor(union, ["SHAPE@AREA"]))

    # Jaccard index
    jaccard = inter_area / union_area if union_area != 0 else 0

    results.append((dist, inter_area, union_area, jaccard))

    # Vyčištění paměti
    arcpy.management.Delete("in_memory/buf_a")
    arcpy.management.Delete("in_memory/buf_b")
    arcpy.management.Delete("in_memory/inter")
    arcpy.management.Delete("in_memory/union")

# Uložení do CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(results)

print("Hotovo! Výstupní CSV:", output_csv)
