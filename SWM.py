import arcpy
import math
import os

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Skola\BP\vizualizace"
scratch_gdb_path = os.path.join(arcpy.env.workspace, "scratch.gdb")

if not arcpy.Exists(scratch_gdb_path):
    arcpy.management.CreateFileGDB(arcpy.env.workspace, "scratch.gdb")

input_features = r"C:\Skola\BP\vrstvy_app_final\zaci_final\skoly2017_polygony.shp"
id_field = "ID"
output_swm = r"C:\Skola\BP\vizualizace\matice_skoly\skoly2017.swm"

d_inner = 500
d_outer = 1000   
exponent = 1   

coords = {}
with arcpy.da.SearchCursor(input_features, [id_field, "SHAPE@X", "SHAPE@Y"]) as cursor:
    for row in cursor:
        coords[row[0]] = (row[1], row[2])

weights = []
ids = list(coords.keys())
for i in ids:
    x_i, y_i = coords[i]
    for j in ids:
        if i == j:
            continue
        x_j, y_j = coords[j]
        dist = math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)  # distance between features

        if dist <= d_inner: 
            weight = 1.0
        elif dist > d_outer:
            weight = 0.0
        else:
            norm_dist = (dist - d_inner) / (d_outer - d_inner)  # distance normalization
            weight = (1 - norm_dist) ** exponent

        if weight > 0:
            weights.append((i, j, weight)) 

temp_table_name = "temp_weights"
temp_table_path = os.path.join(scratch_gdb_path, temp_table_name)
if arcpy.Exists(temp_table_path):
    arcpy.management.Delete(temp_table_path)

arcpy.management.CreateTable(scratch_gdb_path, temp_table_name)
arcpy.management.AddField(temp_table_path, "ID", "LONG")     
arcpy.management.AddField(temp_table_path, "NID", "LONG")   
arcpy.management.AddField(temp_table_path, "WEIGHT", "DOUBLE")

with arcpy.da.InsertCursor(temp_table_path, ["ID", "NID", "WEIGHT"]) as cursor:
    for row in weights:
        cursor.insertRow(row)

arcpy.stats.GenerateSpatialWeightsMatrix(
    Input_Feature_Class=input_features,
    Unique_ID_Field=id_field,
    Output_Spatial_Weights_Matrix_File=output_swm,
    Conceptualization_of_Spatial_Relationships="CONVERT_TABLE",
    Input_Table=temp_table_path,
    Row_Standardization="ROW_STANDARDIZATION"
)