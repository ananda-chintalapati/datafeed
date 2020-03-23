from matilda_datafeed.model import Alert, IssueLink

il = IssueLink()
il.link = "http://google.com"
il.type = "Performance"

alert = Alert()
alert.alertId = 123
alert.summary = 'Summary goes here'
alert.description = 'description'
alert.issueLinks = [il.__dict__]

print (alert.__dict__)