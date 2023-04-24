import arcpy
import csv
import requests
import logging
from SpatialEtl import SpatialEtl

class GSheetsEtl(SpatialEtl):
    config_dict = None
    def __init__(self,config_dict):
        self.config_dict = config_dict

    def extract(self):
        logging.info("Extracting addresses from spreadsheet")

        r = requests.get(self.config_dict.get("remote_url"))
        r.encoding = "utf-8"
        data = r.text
        with open(rf"{self.config_dict.get('proj_dir')}\address.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        transformed_file = open(f"{self.config_dict.get('proj_dir')}new_addresses.csv", "w")
        transformed_file.write("X,Y,Type\n")
        with open(rf"{self.config_dict.get('proj_dir')}\addresses.csv", "r") as partial_file:
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

    def load(self):
        #set environment
        arcpy.env.workspace = rf"{self.config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
        arcpy.env.overwriteOutput = True
        in_table = f"{self.config_dict.get('proj_dir')}new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)
        logging.info(arcpy.GetCount_management(out_feature_class))


    def process(self):
        self.extract()
        self.transform()
        self.load()
