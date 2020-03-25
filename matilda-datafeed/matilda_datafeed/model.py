
class IssueLink():

    linkType = None
    link = None

class Alert():

    alertId = None
    summary = None
    description = None
    createOn = None
    updateOn = None
    closedOn = None
    sourceAlertId = None
    status = None
    severity = None
    issueLinks = []
    createdBy = None
    source = None
    hostId = None
    ipAddress = None
    applicationId = None
    serviceId = None
    type = None

class Application():

    applicationId = None
    clientApplicationId = None
    name = None
    organization = None
    portfolioOwner = None
    owner = None
    director = None
    custodian = None
    category = None
    criticality = None

class Host():

    hostId = None
    state = None
    datacenter = None
    hostname = None
    externalSerialNumber = None
    instanceType = None
    platform = None
    make = None
    model = None
    ipAddress = None
    ipDomain = None
    operatingSystem = None
    osVersion = None
    cloudProvider = None
    environment = None
    deviceType = None
    cores = None
    allocatedMemory = None
    allocatedStorage = None
    osEosl = None
    hwEosl = None

class ApplicationHost():

    applicationId = None
    environmentId = None
    hostId = None

class Environment():

    environmentId = None
    applicationId = None
    name = None
    type = None
