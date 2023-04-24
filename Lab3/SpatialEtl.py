import logging
#push
class SpatialEtl:
    def __init__(self,config_dict):
        self.config_dict = config_dict

    def extract(self):
        logging.info(f"Extracting data from {self.config_dict.get('remote_url')}"
              f" to {self.config_dict.et('proj_dir')}")
    def tranform(self):
        logging.info(f"Tranforming data from {self.config_dict('format')}")
    def load(self):
        logging.info(f"Loading data to {self.config_dict('project_dir')}")