import os
import json
import configparser

CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), '../new_relic/config.ini'))
NR_EP_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), '../new_relic/nr_endpoints.ini'))

def get_lookup_data(section, name):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        print ('CONFIG FILE ' + CONFIG_FILE)
        return config.get(section, name)
    except:
        return None

def get_endpoint(key):
    config = configparser.ConfigParser()
    config.read(NR_EP_FILE)
    try:
        return config.get(key)
    except:
        return None
