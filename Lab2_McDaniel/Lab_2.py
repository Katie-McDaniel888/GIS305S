import arcpy
from etl.GSheetEtl import GSheetsEtl
import requests
from SpatialEtl import SpatialEtl
import yaml

def setup():
    arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
    with open('config/wnvoutbreak.yaml') as f:config_dict = yaml.load(f, loader=yml.FullLoader)
    return config_dict
def etl():
    print("Take the survey")
    etl_instance=GSheetsEtl("https://foo_bar.com", "C:/Users/my.gdb", "C:/Users", "GSheets")
    etl_instance.process()
# Create default workspace
class GSheetsEtl(SpatialEtl):
    config_dict = None
    def __init__(self,config_dict):
        super().__init__(self.config_dict)
    def extract(self):
        print(f"Extracting addresses from {self.config_dict.get('remote_url')}" f"to {self.config_dict.get('proj_dir')}")
        #file = urllib.request.urlopen("https://docs.google.com/forms/d/e/1FAIpQLSe1QzJGuFFAb0xQi2VxWE9bmc85Oxv4a3SNnuAvgVgaZgVySg/viewform?usp=sf_link)
        r = requests.get(self.config_dict.get('remote_url'))
    def load(self):
        #set environment
        arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
        arcpy.env.orderwriteOutput = True
        in_table = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)
        prnt(arcpy.GetCount_management(out_feature_class))
    def process(self):
        self.extract()
        self.transform()
        self.load()
class SpatialEtl:
    def __init__(self,config_dict):
        self.config_dict = config_dict
    def extract(self):
        print(f"Extracting data from {self.config_dict.get('remote_url')}" f"to {self.config_dict.get('proj_dir')}")
    def transform(self):
        print(f"Transforming {self.config_dict.get('data_format')}")
    def load (self):
        print(f"Loading data into {self.config_dict.get('proj_dir')}")

# Add layers
input_path = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb{layer_name}"

mosquito=input_path.format(layer_name=r"\Mosquito_Larval_Sites")
osmp=input_path.format(layer_name=r"\OSMP_Properties")
lakes_reservoirs=input_path.format(layer_name=r"\Lakes_and_Reservoirs___Boulder_County")
wetlands=input_path.format(layer_name=r"\Wetlands")

list_lyrs = ["buff_lakes_reservoirs", "buff_mosquitos", "buff_wetlands", "buff_osmp"]

def buffer(layer_name, bufDist):
    # Buffer the incoming layer by the buffer distance
    arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\WestNileOutbreak.gdb"

    arcpy.Buffer_analysis(mosquito, "buff_mosquitos", "1500 Feet")
    arcpy.Buffer_analysis(osmp, "buff_osmp", "1500 Feet")
    arcpy.Buffer_analysis(lakes_reservoirs, "buff_lakes_reservoirs", "1500 Feet")
    arcpy.Buffer_analysis(wetlands, "buff_wetlands", "1500 Feet")

    print(f"Buffering{layer_name} to generate {out_feature_class}")

def intersect(list_lyrs):
    arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\WestNileOutbreak.gdb"
    # Ask the user to name the output layer
    lyr_name = input('What is the Name of the layer')
    # run an intersect operation on multiple input layers
    arcpy.Intersect_analysis(list_lyrs)
    # Return the result output layer
    return lyr_name

def main():
    # define default workspace
    arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
    list_lyrs = ["buff_lakes_reservoirs", "buff_mosquitos", "buff_wetlands", "buff_osmp"]
    output_lyr_name= intersect(list_lyrs)

def spatial_join():
    # Spatial Join
    join_features = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\buff_lakes_reservo_Intersect1"
    target_features = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\Addresses"
    out_feature_class = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\Spatial_Join"
    arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)

    print(f"My spatial join method")
def erase():
    eraseOutput = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\buff_avoid_points"
    arcpy.analysis.Erase(buff_avoid_points, eraseOutput)
if __name__ == '__main__':
   config_dict = setup()
   print(config_dict)
   etl()
   main()

