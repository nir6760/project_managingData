# Import libraries
from configparser import ConfigParser
from pathlib import Path

from configuration.config import *


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parents[1]

# get configurations for connecting DB
def configFromIniFile(config_db_path):
    section = 'postgresql'
    if len(config_db_path) > 0 and len(section) > 0:
        # Create an instance of ConfigParser class
        config_parser = ConfigParser()
        # Read the configuration file
        config_parser.read(config_db_path)
        # If the configuration file contains the provided section name
        if config_parser.has_section(section):
            # Read the options of the section
            config_params = config_parser.items(section)
            # Convert the list object to a python dictionary object
            # Define an empty dictionary
            db_conn_dict = {}
            # Loop in the list
            for config_param in config_params:
                # Get options key and value
                key = config_param[0]
                value = config_param[1]
                # Add the key value pair in the dictionary object
                db_conn_dict[key] = value
            # Get connection object use above dictionary object
            return db_conn_dict

def config_params():
    db_conn_dict = {'host': host, 'database': database, 'user': user, 'password': password, 'port': port}
    return db_conn_dict
