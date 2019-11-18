from jira import JIRA
from app import db
from app.models import Issue
from time import strptime,strftime

server='http://10.9.11.254'
jira = JIRA(server,basic_auth=('shihaonan','haonan1124'))
need_fields = 'status,created,summary,creator'

# 获取全部数据
def jira_get_all():
    jql = 'project = DSG AND issuetype in (Bug, 财务需求,需求) AND creator in (membersOf(产品组))'
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

# 获取过去1天的增量数据
def jira_get_new():
    jql = 'project = DSG AND issuetype in (Bug, 财务需求, 需求) AND created >= -1d AND creator in (membersOf(产品组))'
    issues = jira.search_issues(jql,fields=need_fields,maxResults=100)
    existing_issues = Issue.query.all()
    # for issue in issues:
    #     for existing_issue in existing_issues:
    #         if issue.key != existing_issue.key:
    #             existing_issue.status = issue.status
    #             existing_issue.summary = issue.summary
    #             db.session.commit()



# a=1
# for issue in issues:
#     print(a,issue.fields.created,issue,issue.fields.summary,issue.fields.creator)
#     print(server+'/browse/'+issue.key)
#     a+=1

