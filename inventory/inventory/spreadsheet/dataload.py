import math
import pandas as pd
from inventory.db import MatildaMongoClient
from matilda_datafeed.model import Application, Host, Environment, ApplicationHost

def load_excel(file_path, sheet_name=None):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print ('Processing ' + str(len(df)) + ' rows of data')
    for index, row in df.iterrows():
        process_entry(row)
    print ('Processing Completed')

def process_entry(row):
    application = create_application_if_not_exist(row)
    environment = create_environment_if_not_exist(application, row)
    host = create_host_if_not_exist(row)
    create_app_host_mapping(application, environment, host)

def get_application_id():
    pass

def create_application_if_not_exist(row):
    vsad = row['VSAD Appl_ID']
    db = MatildaMongoClient()
    application = db.get_application_by_vasd(vsad)
    if application is None:
        application = _prepare_application(row)
        return db.save_application(application.__dict__)
    else:
        return str(application['_id'])

def create_environment_if_not_exist(applicationId, row):
    db = MatildaMongoClient()
    environment = db.get_environment_by_name_application(applicationId, row['Environment'])
    if environment is None:
        env = Environment()
        env.applicationId = applicationId
        env.name = row['Environment']
        env.type = str(row['Pivot Table Environment Tracking'])
        return db.create_environment(env.__dict__)
    return str(environment['_id'])


def _prepare_application(row):
    application = Application()
    application.organization = row['Portfolio Organization']
    application.portfolioOwner = row['App_Portfolio']
    application.owner = row['App_Owner_Name']
    application.director = row['App_Director_Name']
    application.custodian = row['App_Custodian_Name']
    application.name = row['App_Name']
    application.clientApplicationId = row['VSAD Appl_ID']
    application.criticality = row['Mission Critical Ranking']
    return application

def _prepare_host(row):
    host = Host()
    host.state = row['Current Status']
    host.datacenter = row['Data Center Name']
    host.hostname = row['Host_Name']
    host.externalSerialNumber = row['External_Serial_No']
    host.instanceType = 'Virtual' if row['Physical Virtual'].lower() == 'v' else 'Physical'
    host.platform = row['OS Platform']
    host.make = row['Make']
    host.model = row['Model']
    host.ipAddress = row['Primary_IP_Address']
    host.ipDomain = row['IPDomainName']
    host.operatingSystem = row['Operating_System']
    host.osVersion = row['OS_Version']
    host.cloudProvider = row['Cloud Identifier']
    host.environment = row['Environment']
    host.deviceType = row['Device Type']
    host.osEosl = row['OS EOSL Date']
    host.hwEosl = row['HW EOSL Date']
    host.cores = row['Total Cores']
    host.allocatedMemory = conv_MB_to_GB(row['AllocatedMemoryMB'])
    host.allocatedStorage = conv_MB_to_GB(row['Allocated StorageMB'])
    return host

def conv_MB_to_GB(input_megabyte):
    gigabyte = float(9.5367431640625E-7)
    convert_gb = float(input_megabyte) / 1024
    return math.ceil(convert_gb)

def create_host_if_not_exist(row):
    db = MatildaMongoClient()
    ip = row['Primary_IP_Address']
    host = db.get_host_by_ip(ip)
    if host is None:
        host = _prepare_host(row)
        return db.save_host(host.__dict__)
    else:
        return str(host['_id'])

def create_app_host_mapping(applicationId, environmentId, hostId):
    db = MatildaMongoClient()
    appHost = ApplicationHost()
    appHost.applicationId = applicationId
    appHost.environmentId = environmentId
    appHost.hostId = hostId
    return db.save_app_host(appHost.__dict__)




