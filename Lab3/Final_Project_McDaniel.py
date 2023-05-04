#Katie McDaniel
#Final - GIS 305
#Spring 2023
import arcpy
import yaml
import logging
from GSheetsEtl import GSheetsEtl


log = logging.getLogger(__name__)
def setup():
    with open(r"C:\Users\ka003737\PycharmProjects\GIS305S\Lab2_McDaniel\Config\wnvoutbreak.yaml") as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict


def etl():
    """etl can be imported as base class definitions for use in extraction, transformation and loading data.
      these classes are created as a csv and is transformed into spatial information for
      further output processing."""
    logging.debug("Etl process has begun")
    print("Start etl process....")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

# Define Buffer
def buffer(buf_lyr):
    layer = aprx.listLayouts()[0]
    units = " feet"
    distance = str(dist) + units

    # Output location path for the buffered layer
    output_layer = f"{layer}_buff"

    # Buffer analysis tool (input variable name, output variable name, distance type string,"FULL", "ROUND", "ALL")
    arcpy.Buffer_analysis(layer, output_layer, distance, "FULL", "ROUND", "ALL")
    print("Buffer created " + output_layer)
    return

#
# Define Intersect
def intersect(int_lyrs):
    log.info('Intersecting')
    # ask user to name output layer
    print(inter_list)
    arcpy.Intersect_analysis(inter_list, output_layer)
    # ask the user to define an output intersect layer and store the results in a variable
    output_layer = f"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\_intersect"

    # run a intersect analysis between the two buffer layer name and store the result in a variable
    # using arcpy.Intersect_analysis

    print("Intersect is complete")
    return output_layer
def erase (erase_points):
    logging.info("Erasing avoid_points to obtain final output")
    print("Erasing layer output created")
    in_features = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\_intersect"
    avoid_points = erase_points
    out_feature_name = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\SpatialJoin_ErasedPoints"
    arcpy.Erase_analysis(in_features, avoid_points, out_feature_name)
    print("Avoid points is erased. Final analysis layer is ready")
    return out_feature_name

def spatial(erase_layer):
    """
    spatial function: creates a spatial join layer with addresses and final analysis layer
    parameters: erase_layer (this is the final analysis layer)
    returns: spj_file (a spatial joined addresses will the final analysis layer)
    """
    logging.info("Spatial joining all the addresses and the final analysis layer.")
    print("Addresses and Final_Analysis layer are being joined")

    target_feature = f"{config_dict.get('proj_dir')}\Addresses"
    join_feature = erase_layer
    spj_file = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\spatial_join"
    arcpy.SpatialJoin_analysis(target_feature, join_feature, spj_file)
    print("Spatial Join has been completed")
    return spj_file


def spatialreference(map_final):
    """
    spatialreference function: will set the map document to a spatial reference of 102653
    (NAD 1983 StatePlane Colorado North FIPS 0501Feet-Northern Colorado State Plane).
    parameters: map_final
    returns: map_final.spatialReference (a spatial referenced map)
    """
    logging.info("Spatial Reference for map document will be set to Northern Colorado State Plane")
    noco = 102653
    state_plane_noco = arcpy.SpatialReference(noco)
    map_final.spatialReference = state_plane_noco
    print("Spatial Reference set to 102653- North Colorado State Plane (feet).")
    return map_final.spatialReference

def exportMap(aprx):
    """
    exportMap function: Sets the spatial reference for the final map document, prints a list
    of the map layouts, prints a list the elements found on the map document and takes the
    Final_Analysis layer-applies a simple renderer (symbology red with transparency of 50% red.
    It then exports a pdf of the final map.
    parameters: aprx (current project)
    returns: a pdf map in the project directory of the yaml file.
    """
    logging.info("Exporting final map has begun.")
    map_final = aprx.listMaps()[0]

    # Setting spatial reference
    spatialreference(map_final)


    # List Map Layout in WNVOutbreak Project
    lyt_list = aprx.listLayouts()[0]
    print(lyt_list.name)

    # List elements within the map layout such as the title, the legend and etc..
    for el in lyt_list.listElements():
        print(el.name)
        if "Title" in el.name:
            el.text = el.text
        if "Date" in el.name:
            el.text = el.text

    # Layers: TargetAddresses
    lyr = map_final.listLayers("Final_Analysis")[0]

    # Get the existing symbol and sets the Final_Analysis layer to red.
    sym = lyr.symbology
    sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
    sym.renderer.symbol.outlineColor = {'RGB': [0, 0, 0, 100]}
    lyr.symbology = sym
    lyr.transparency = 10

    # Save all the aprx to the
    aprx.save()

    # Export final map to a pdf using the user input name.
    lyt_list.exportToPDF(f"{config_dict.get('proj_dir')}\\final_map")
    return
# Define Main
def main():
    log.info('Starting West Nile Virus Simulation')
    arcpy.env.workspace = f"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    # Define variables
    LayerList = ["Mosquito_Larval_Sites", "Wetlands", "OSMP_Properties",
                 "Lakes_and_Reservoirs___Boulder_County", "avoid_points"]
    # Call buffer
    for layer in LayerList:
        dist = 1500
        buffer = (layer,dist)

    # Call Intersect
    logging.debug("Intersect...")
    inter_list = ["buff_mosquitos", "buff_wetlands", "buff_osmp",
                  "buff_lakes_reservoirs", "avoid_points_buff"]
    try:
        output_intersectlayer = intersect(inter_list)
        print(f"{output_intersectlayer}")
    except:
        print("Something went wrong with the intersect all buffered layers function.")
    #Intersect buffered layers with the avoid_points layer
    logging.debug("Intersect all buffered layers and the avoid points layer for final analysis layer.")
    inter_list2 = ["Intersected Areas", "avoid_points_buff"]
    outputlayer_avpt = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\intersect_avpt"
    try:
        arcpy.Intersect_analysis(inter_list2, outputlayer_avpt)
        print("Intersect avoid points layer complete.")
    except:
        print("Something went wrong with the intersect between all buffered layers and avoid points layers.")
        # Erase avoid_points_buffer layer from the intersect layer, display final areas to be sprayed
    logging.debug("Erase new address points from spatial join layer.")
    erase_points = "intersect_avpt"
    try:
        erase_layer = erase(erase_points)
        print(f"Erases new address file from spatial join: {erase_layer}")
    except:
        print("Something went wrong with erasing avoid_points from the intersect.")

    # Spatial Join of all the buffered layers.
    logging.debug("Spatial Join all the buffered layers.")
    try:
        finaloutput_spjlayer = spatial(erase_layer)
        print(f"New Spatial Join Layer named: {finaloutput_spjlayer}")
    except:
        print("Something went wrong with the spatial join for all  buffered layers and addresses")

    # Clip Addresses to final analysis layer.
    try:
        logging.debug("Clip addresses to final analysis layer to get target addresses to contact for spraying")
        TargetAddresses = arcpy.Clip_analysis("Addresses", erase_layer, "Target_Addresses")
        print(f"Final target address layer has been completed:{TargetAddresses}")

        # Number of addresses to be contacted.
        logging.debug("GetCount for target address file.")
        address_count = arcpy.management.GetCount(TargetAddresses)
        print(f"Number of addresses to be contacted for mosquito spraying:{address_count}")

        # Convert Target Addresses feature class to a shapefile
        logging.debug("Convert feature layer to a shapefile.")
        TargetAddresses_shape = arcpy.conversion.FeatureClassToShapefile(TargetAddresses,
                                                            f"{config_dict.get('proj_dir')}\\TargetAddresses_shape")
        print(f"Target Address layer has been converted to a shapefile: {TargetAddresses_shape}")
    except:
        print("Something went wrong with the clipping addresses to final analysis layer.")
    # upload project to ArcGIS Pro
    #logging.info("Creating the layout and saving final map to a pdf.")
    #aprx = arcpy.mp.ArcGISProject(f"{config_dict.get('proj_dir')}Katie_McDaniel_Lab1.aprx")
    #map = aprx.listMaps()[0]
    #map = exportMap(aprx)

    print("Final Map Complete")
    arcpy.env.overwriteOutput = True
if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    main()

