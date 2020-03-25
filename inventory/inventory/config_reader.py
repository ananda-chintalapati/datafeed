import os
import json
import configparser

CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), '../inventory/config.ini'))

def get_lookup_data(section, name):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        return config.get(section, name)
    except:
        return None
