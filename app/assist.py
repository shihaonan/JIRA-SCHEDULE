from jira import JIRA
from app import db
from app.models import Issue
from time import strptime,strftime

server='http://10.9.11.254'
jira = JIRA(server,basic_auth=('shihaonan','haonan1124'))

jql = 'project = DSG AND issuetype in (Bug, 需求) AND creator in (membersOf(产品组))'
need_fields = 'status,created,summary,creator'

def jira_connect():
    issues = jira.search_issues(jql,fields=need_fields,maxResults=1000)
    for issue in issues:
        new_issue = Issue(
            key=issue.key,
            status=issue.fields.status.name,
            created_time= strftime("%Y-%m-%d", strptime(issue.fields.created[0:10],'%Y-%m-%d')),
            summary=issue.fields.summary,
            creator=issue.fields.creator.displayName,
            url=str(server+'/browse/'+issue.key)
        )
        db.session.add(new_issue)
        db.session.commit()

# jira_connect()


# a=1
# for issue in issues:
#     print(a,issue.fields.created,issue,issue.fields.summary,issue.fields.creator)
#     print(server+'/browse/'+issue.key)
#     a+=1

