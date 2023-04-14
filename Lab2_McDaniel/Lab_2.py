import arcpy
import requests
import yaml
import csv

class SpatialEtl:
    def __init__(self,config_dict):
        self.config_dict = config_dict
    def extract(self):
        print(f"Extracting data from {self.config_dict.get('remote_url')}" f"to {self.config_dict.get('proj_dir')}")
    def transform(self):
        print(f"Transforming {self.config_dict.get('data_format')}")
    def load (self):
        print(f"Loading data into {self.config_dict.get('proj_dir')}")
# Create default workspace
class GSheetsEtl(SpatialEtl):
    config_dict = None
    def __init__(self,config_dict):
        super().__init__(config_dict)

    def extract(self):
        print(f"Extracting addresses from {self.config_dict}")
        # file = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")

        r = requests.get(self.config_dict.get("remote_url"))
        r.encoding = "utf-8"
        data = r.text
        with open(r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\addresses.csv", "w") as output_file:
            output_file.write(data)
    def load(self):
        #set environment
        arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\WestNileOutbreak.gdb"
        arcpy.env.overwriteOutput = True
        in_table = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)
        print(arcpy.GetCount_management(out_feature_class))

    def transform(self):
        transformed_file = open(r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\new_addresses.csv", "w")
        transformed_file.write("X,Y,Type\n")
        with open(r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\addresses.csv", "r") as partial_file:
            csv_dict = csv.DictReader(partial_file, delimiter=',')
            for row in csv_dict:
                address = row["Street Address"] + " Boulder CO"
                print(address)
                geocode_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + address + "&benchmark=2020&format=json"
                print(geocode_url)
                r = requests.get(geocode_url)

                resp_dict = r.json()
                x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                transformed_file.write(f"{x},{y},Residential\n")

        transformed_file.close()
    def process(self):
        self.extract()
        self.transform()
        self.load()

def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    arcpy.env.workspace = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb"
    return config_dict

def buffer(layer_name, bufDist):
    # Buffer the incoming layer by the buffer distance
    arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\WestNileOutbreak.gdb"

    arcpy.Buffer_analysis(mosquito, "buff_mosquitos", "1500 Feet")
    arcpy.Buffer_analysis(osmp, "buff_osmp", "1500 Feet")
    arcpy.Buffer_analysis(lakes_reservoirs, "buff_lakes_reservoirs", "1500 Feet")
    arcpy.Buffer_analysis(wetlands, "buff_wetlands", "1500 Feet")
    arcpy.Buffer_analysis(avoid_points, "buff_avoid_points", "1500 Feet")

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
    arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\WestNileOutbreak.gdb"
    list_lyrs = ["buff_lakes_reservoirs", "buff_mosquitos", "buff_wetlands", "buff_osmp"]
    output_lyr_name= intersect(list_lyrs)
    input_path = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb{layer_name}"

    mosquito = input_path.format(layer_name=r"\Mosquito_Larval_Sites")
    osmp = input_path.format(layer_name=r"\OSMP_Properties")
    lakes_reservoirs = input_path.format(layer_name=r"\Lakes_and_Reservoirs___Boulder_County")
    wetlands = input_path.format(layer_name=r"\Wetlands")
    avoid_points = input_path.format(layer_name=r"\avoid_points")

    list_lyrs = ["buff_lakes_reservoirs", "buff_mosquitos", "buff_wetlands", "buff_osmp", "buff_avoid_points"]
    eraseOutput = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\buff_avoid_points"
    arcpy.analysis.Erase(output_lyr_name, eraseOutput)
def spatial_join():
    # Spatial Join
    join_features = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\buff_lakes_reservo_Intersect1"
    target_features = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\Addresses"
    out_feature_class = f"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\Spatial_Join"
    arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class)

    print(f"My spatial join method")

if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    gsheetsetl = GSheetsEtl(config_dict)
    gsheetsetl.process()
    main()
