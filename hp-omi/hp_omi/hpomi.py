import xmltodict
import json
import requests
from datetime import datetime, timedelta
from hp_omi import config_reader as cr
from matilda_datafeed.model import Alert, IssueLink
from matilda_datafeed import db as df_db

def get_and_save_alerts():
    alerts = get_events()
    process_events(alerts)

def get(url):
    headers = {'Content-type':'application/json'}
    try:
        resp = requests.get(url=url, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            return None
    except Exception as e:
        return None

def get_url(param):
    url = cr.get_lookup_data('HPOMI', 'base_url') + cr.get_lookup_data('HPOMI', param)
    return url

def convert_xml_to_dict(data):
    doc = xmltodict.parse(data, process_namespaces=False)
    resp = json.loads(json.dumps(doc))
    return resp

def round_time(dt=None, round_to=60):
   if dt == None:
       dt = datetime.now()
   seconds = (dt - dt.min).seconds
   rounding = (seconds+round_to/1) // round_to * round_to
   return dt + timedelta(0, rounding-seconds, -dt.microsecond)

def get_from_dt():
    dt = round_time()
    start_dt = dt - timedelta(minutes=3)
    return start_dt

def get_events():
    url = get_url('events') + get_from_dt()
    resp = get(url)
    return resp

def process_events(events):
    for event in events:
        alert = prepare_alert_payload(event)
        df_db.save_update_alert(alert.sourceAlertId, alert)


def get_host_id(host_ip):
    host_id = None
    if host_ip is not None and host_ip != '':
        host = df_db.get_host(host_ip)
        if host is not None:
            host_id = host.get('id')
    return host_id

def prepare_alert_payload(event, host_id=None, application_id=None):
    alert = Alert()
    alert.hostId = host_id
    alert.type = 'host'
    alert.createdOn = event.time_first_received
    alert.applicationId = get_application_id(event)
    alert.status = event.state
    alert.sourceAlertId = event.id
    alert.source = 'hp-omi'
    alert.ipAddress = get_ip_address(event.node_ref.node)
    alert.severity = event.severity
    alert.summary = event.title
    alert.description = get_description(event)
    alert.issueLinks = get_issue_links(event)
    return alert

def get_ip_address(node):
    ip_list = node.get('ip_address_list')
    if ip_list is None:
        ip_list = node.get('host_key')
    if ip_list is not None:
        ip = ip_list.split(" ")
        return ip[0]
    return None

def get_description(event):
    msg = ''
    msg += event.title + '\n'
    msg += event.original_data + '\n'

def get_issue_links(event):
    links = []

    issue = IssueLink()
    issue.linkType = "Drilldown URL"
    issue.link = event.drilldown_url
    links.append(issue)

    history = IssueLink()
    history.linkType = "History"
    history.link = event.history_line_list_ref.target_href
    links.append(history)

def get_application_id(event):
    app_name = get_custom_attribute(event, 'AppName')
    if app_name is not None:
        application = df_db.get_application_by_vasd(app_name)
        if application is not None:
            return application['id']
        else:
            return app_name
    return None

def get_custom_attribute(event, value):
    custom_attributes = event.custom_attribute_list.custom_attribute
    for attribute in custom_attributes:
        if attribute.name.lower() == value.lower():
            return attribute.value
    return None