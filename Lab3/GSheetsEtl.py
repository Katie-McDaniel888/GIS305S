import arcpy
import csv
import requests
import logging

import GSheetsEtl
from SpatialEtl import SpatialEtl
my_etl = GSheetsEtl({})
print(my_etl.__doc__)
help(my_etl)

GSheetsEtl performs an extract, transform, and load process using a URL to a Google Spreadsheet. The Spreadsheet must contain an address and zipcode column.
Help on GSheetsEtl in module etl.GSheetsEtl object:
class GSheetsEtl(etl.SpatialEtl.SpatialEtl)
        GSheetsEtl(config_dict)
        GSheetsEtl performs an extract, transform, and load process using a URL to a Google Spreadsheet
class GSheetsEtl(SpatialEtl):
    """
    GSheetsEtl performs an extract, transform and load process uing a URL to a google spreadsheet. The spreadsheet must contain an address and zipcode column
    Parameters:
    config_dict (dictionary): A dictionary containing a remote_URL key to the google spreadsheet and web geocoding service
    """

    # A dictionary of configuration keys and values
    config_dict = None
    def __init__(self,config_dict):
        self.config_dict = config_dict
#push
    def extract(self):
        """
        Extracting data from a Google spreadsheet and save it as a local file
        """
        logging.info("Extracting addresses from spreadsheet")

        r = requests.get(self.config_dict.get("remote_url"))
        r.encoding = "utf-8"
        data = r.text
        with open(rf"{self.config_dict.get('proj_dir')}\address.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        """
        Transforming the data from addresses to a geocoded address for map placement
        """
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
        """
        Load the new geocoded data into the map as a point
        """
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
