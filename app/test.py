from jira import JIRA
from time import strptime,strftime
from app.models import Issue
from app import db
from datetime import date,timedelta

server='http://10.9.11.254'
jira = JIRA(server,basic_auth=('shihaonan','haonan1124'))

jql = 'project = DSG AND issuetype in (Bug, 需求) AND creator in (membersOf(产品组))'
need_fields = 'status,created,summary,creator'
def jira_connect():
    issues = jira.search_issues(jql,fields=need_fields,maxResults=10)
    for issue in issues:
        print(
            issue.key,
            issue.id,
            issue.fields.status,
            strftime("%Y-%m-%d", strptime(issue.fields.created[0:10],'%Y-%m-%d')),
            issue.fields.summary,
            issue.fields.creator,
            str(server+'/browse/'+issue.key)
        )

# jira_connect()

# issue = jira.issue('DSG-12003')
# print(issue.id)

last_time = date.today()
print(last_time)
print(type(last_time))