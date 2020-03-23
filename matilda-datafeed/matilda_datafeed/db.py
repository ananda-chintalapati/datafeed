from pymongo import MongoClient
from matilda_newrelic import config_reader
from bson.objectid import ObjectId

def get_client():
    client = MongoClient(config_reader.get_lookup_data('MONGO', 'host'),
                         int(config_reader.get_lookup_data('MONGO', 'port')))
    db = client[config_reader.get_lookup_data('MONGO', 'database')]
    return db

def get_host(ip_address, host_id=None):
    group = get_client()['host']
    host_data = None
    if host_id is not None:
        return group.find_one({'_id': ObjectId(host_id)})
    elif host_data is None and ip_address is not None:
        return group.find_one({'ip_address': ip_address})
    return None

def get_host_application(host_id):
    group = get_client()['application_host']
    return group.find_one({'hostId': host_id})

def get_application_by_vasd(vasd):
    group = get_client()['application']
    return group.find_one({'clientApplicationId':vasd})


def save_update_alert(alert_id, data):
    group = get_client()['alerts']
    alert = group.find_one_and_update({"source_alert_id": alert_id}, {"$set": data}, upsert=True)
    return alert