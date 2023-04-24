import arcpy
import requests
import csv

def extract(self):
    print(f"Extracting addresses from {self.remote} to {self.local_dir}")
    #file = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")

    r = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")
    r.encoding = "utf-8"
    data = r.text
    with open(r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\addresses.csv", "w") as output_file:
        output_file.write(data)


def transform(self):
    print(f"Transforming {self.data_format} Add City, State")

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


def load(self):
    # Description: Creates a point feature class from input table

    # Set environment settings
    arcpy.env.workspace = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab1\Katie_McDaniel_Lab1\Katie_McDaniel_Lab1.gdb\\"
    arcpy.env.overwriteOutput = True

    # Set the local variables
    in_table = r"C:\Users\ka003737\Downloads\Spring_2023\GIS3005\Lab 2\new_addresses.csv"
    out_feature_class = "avoid_points"
    x_coords = "X"
    y_coords = "Y"


    # Make the XY event layer...
    arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

    # Print the total rows
    print(f"Loading data into {self.destination}" "arcpy.GetCount_management(out_feature_class)")


if __name__ == "__main__":
    extract()
    transform()
    load()