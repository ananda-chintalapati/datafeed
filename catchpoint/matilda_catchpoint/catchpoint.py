from matilda_catchpoint import db
from matilda_datafeed.model import Alert, IssueLink
from matilda_datafeed import db as df_db

def get_and_save_alerts():
    alerts = get_alerts()
    save_alerts(alerts)

def get_alerts():
    cp_alerts = db.get_cp_alerts()
    return cp_alerts

def save_alerts(cp_alerts):
    for alert in cp_alerts:
        host = None
        host_id = None
        if cp_alerts.node_ip is not None and cp_alerts.node_ip != '':
            host = df_db.get_host(cp_alerts.node_ip)
            if host is None:
                if cp_alerts.node_host_ip is not None and cp_alerts.node_host_ip != '':
                    host = df_db.get_host(cp_alerts.node_host_ip)
        if host is not None:
            host_id = host.get('id')
        application = df_db.get_application_by_vasd(cp_alerts.vasd)
        alert = prepare_alert_payload(alert, host_id, application.get('id'))
        df_db.save_update_alert(alert.sourceAlertId, alert)

def prepare_alert_payload(cp_alert, host_id=None, application_id=None):
    alert = Alert()
    alert.hostId = host_id
    alert.type = cp_alert.test_type
    alert.createdOn = cp_alert.report_time
    alert.applicationId = application_id or cp_alert.vsad
    alert.status = get_status(cp_alert.level_name)
    alert.sourceAlertId = cp_alert.test_id
    alert.source = 'catchpoint'
    alert.ipAddress = cp_alert.node_host_ip or cp_alert.node_ip
    if cp_alert.level_name.lower() == 'improved':
        alert.closedOn = cp_alert.processing_time
        alert.status = 'closed'
    alert.severity = cp_alert.level_name
    alert.summary = get_summary(cp_alert)
    alert.description = get_description(cp_alert)
    alert.issueLinks = get_issue_links(cp_alert)
    return alert

def get_status(level):
    if level is not None and level.lower() == 'improved':
        return 'closed'
    return 'open'

def get_summary(alert):
    summary = alert.vasd + ' - '
    summary = summary + alert.test_name + " : " + "test_description" + ' - ' + alert.alert_type
    return summary

def get_description(alert):
    description = ''
    description = description + alert.description + ' - ' + alert.test_type + '\n'
    description = description + 'Node : ' + alert.node + '\n'
    description = description + 'Company : ' + alert.company + '\n'
    description = description + 'Prod Name : ' + alert.prod_name + '\n'
    description = description + 'Error : ' + alert.error + '\n'
    description = description + 'Cause : ' + alert.cause + '\n'
    return description

def get_issue_links(alert):
    issue_links = []

    issue = IssueLink()
    issue.linkType = 'Test Link'
    issue_links = alert.test_link
    issue_links.append(issue)

    perf_issue = IssueLink()
    perf_issue.linkType = 'Test Performance Link'
    perf_issue = alert.test_perf_url
    issue_links.append(perf_issue)

    wf_issue = IssueLink()
    wf_issue.linkType = 'Test Waterfall Link'
    wf_issue = alert.test_waterfall_url
    issue_links.append(wf_issue)

    return issue_links