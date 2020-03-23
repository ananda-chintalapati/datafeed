import re
from datetime import datetime, timedelta
import requests
from matilda_newrelic import config_reader as cr
from matilda_datafeed import db
from matilda_datafeed.model import Alert, IssueLink

DATE_FILE='end_date.out'

def get(url, key_type='api'):
    headers = {'Content-type':'application/json'}
    if key_type == 'api':
        headers['X-Api-Key'] = cr.get_lookup_data('NEWRELIC', 'api_token')
    else:
        headers['X-Query-Key'] = cr.get_lookup_data('NEWRELIC', 'query_key')
    try:
        resp = requests.get(url=url, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            return None
    except Exception as e:
        return None

def get_url(param):
    url = cr.get_endpoint('base_url') + cr.get_endpoint(param)
    return url

def get_view_url(param):
    return cr.get_endpoint(param)

def round_time(dt=None, round_to=60):
   if dt == None:
       dt = datetime.now()
   seconds = (dt - dt.min).seconds
   rounding = (seconds+round_to/1) // round_to * round_to
   return dt + timedelta(0, rounding-seconds, -dt.microsecond)

def get_time_query():
    dt = round_time()
    start_dt = dt - timedelta(minutes=3)
    end_dt = dt - timedelta(minutes=2)
    return 'start_date=' + start_dt.strftime("%Y-%m-%dT%H:%M:%S") + '&end_date=' + end_dt.strftime("%Y-%m-%dT%H:%M:%S")

def get_and_save_alerts():
    violations = get_violations()
    save_violations(violations)

def get_violations():
    url = get_url('violations') + '?' + get_time_query()
    violation_list = get(url)
    return violation_list

def save_violations(violation_list):
    for violation in violation_list:
        host = None
        application_host = None
        entity = violation.get('entity')
        if entity['type'] == 'Host' and entity['product'] == 'Infrastructure':
            host = db.get_host(get_host_address(entity['name']))
            application_host = db.get_host_application(host['id'])
        alert = prepare_alert_payload(violation, entity['type'].lower(), host['id'], application_host['applicationId'])
        db.save_update_alert(violation['id'], alert)

def prepare_alert_payload(violation, type='host', host_id=None, application_id=None):
    alert = Alert()
    alert.hostId = host_id
    alert.type = type
    alert.createdOn = violation['opened_at']
    alert.applicationId = application_id
    alert.status = 'open'
    alert.sourceAlertId = violation['id']
    alert.source = 'newrelic'
    alert.ipAddress = get_host_address(violation['entity'].get('name'))
    if hasattr(violation, 'closed_at'):
        alert.closedOn = violation['closed_at']
        alert.status = 'closed'
    alert.severity = violation['priority']
    alert.summary = violation['label']
    alert.description = violation['label']
    alert.issueLinks = prepare_issue_links(violation['links'].get('incident_id'), violation['links'].get('condition_id'))
    return alert

def get_host_address(host):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if '-' in host:
        host_list = host.split('-')
        if len(host_list) == 4 and regex.search(host) == None:
            return '.'.join(host_list)
        else:
            return host
    elif regex.search(host) == None:
        return host
    return host

def prepare_issue_links(incident_id=None, condition_id=None):
    links = []
    if incident_id is not None:
        incident = IssueLink()
        incident.type = 'Incident'
        incident.link = get_view_url('incident_view') + incident_id
        links.append(incident.__dict__)
    if condition_id is not None:
        condition = IssueLink()
        condition.type = 'Condition'
        condition.link = get_view_url('condition_view') + incident_id
        links.append(condition.__dict__)
    return links

def get_policies():
    pass

def get_alerts():
    pass

def get_inicident():
    pass

