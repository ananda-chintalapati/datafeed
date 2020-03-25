from pymongo import MongoClient
from inventory import config_reader
from bson.objectid import ObjectId

class MatildaMongoClient():
    
    def __init__(self):
        self.client = MongoClient(config_reader.get_lookup_data('MONGO', 'host'),
                             int(config_reader.get_lookup_data('MONGO', 'port')))
        self.db = self.client[config_reader.get_lookup_data('MONGO', 'database')]


    def create_application(self, data):
        try:
            group = self.db['application']
            application = group.save(data)
            return application
        finally:
            self.client.close()
    
    def get_application_by_vasd(self, vsad):
        try:
            group = self.db['application']
            return group.find_one({'clientApplicationId':vsad})
        finally:
            self.client.close()
    
    def create_environment(self, data):
        try:
            env_type = data.get('type')
            if env_type is not None and env_type.lower() == 'production':
                data['isDefault'] = True
            group = self.db['environment']
            return group.save(data)
        finally:
            self.client.close()
    
    def get_environment_by_name_application(self, applicationId, name):
        try:
            group = self.db['environment']
            return group.find_one({'applicationId': applicationId, 'name': name})
        finally:
            self.client.close()
    
    def get_host_by_ip(self, ip):
        try:
            group = self.db['host']
            return group.find_one({'ipAddress': ip})
        finally:
            self.client.close()
    
    def save_host(self, data):
        try:
            env_type = self.db['host']
            return env_type.save(data)
        finally:
            self.client.close()
    
    def save_application(self, data):
        try:
            env_type = self.db['application']
            return env_type.save(data)
        finally:
            self.client.close()
    
    def get_default_env(self, applicationId):
        try:
            group = self.db['environment']
            return group.find_one({'applicationId': applicationId, 'isDefault': True})
        finally:
            self.client.close()
    
    def save_app_host(self, data):
        try:
            env_type = self.db['application_host']
            return env_type.save(data)
        finally:
            self.client.close()