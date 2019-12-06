from jira import JIRA
from app import db
from app.models import Issue,LastTime,ProStatus
from time import strptime,strftime
from datetime import date,timedelta

server='http://10.9.11.254'
jira = JIRA(server,basic_auth=('shihaonan','haonan1124'))
need_fields = 'status,created,summary,creator,resolutiondate,updated'


# 获取全部数据
def jira_get_all():
    jql = 'project = DSG AND issuetype in (Bug, 财务需求,需求) AND creator in (membersOf(产品组))'
    issues = jira.search_issues(jql,fields=need_fields,maxResults=1000)
    all_issues_num = 0
    for issue in issues:
        if issue.fields.resolutiondate:
            issue_resolutiondate = strftime("%Y-%m-%d", strptime(issue.fields.resolutiondate[0:10], '%Y-%m-%d'))
        else:
            issue_resolutiondate = None
        new_issue = Issue(
            key=issue.key,
            jira_id=int(issue.id),
            status=issue.fields.status.name,
            created_time= strftime("%Y-%m-%d", strptime(issue.fields.created[0:10],'%Y-%m-%d')),
            resolutiondate=issue_resolutiondate,
            updated=strftime("%Y-%m-%d", strptime(issue.fields.updated[0:10], '%Y-%m-%d')),
            summary=issue.fields.summary,
            creator=issue.fields.creator.displayName,
            url=str(server+'/browse/'+issue.key)
        )
        db.session.add(new_issue)
        db.session.commit()
        all_issues_num += 1
    return '获取全部记录，共查询了 %s 条' % all_issues_num


# 获取上次请求时间到现在的增量数据,本地已存在的更新字段，本地不存在的新建记录
def jira_get_new():
    last_time = LastTime.query.first()
    if not last_time:
        last_time = LastTime(last_request_time=date.today())
        db.session.add(last_time)
        db.session.commit()
    msg1 = '上次请求时间：%s 。' % last_time.last_request_time
    jql = 'project = DSG AND issuetype in (Bug, 财务需求, 需求) AND updated >= %s AND creator in (membersOf(产品组))' % last_time.last_request_time
    issues = jira.search_issues(jql, fields=need_fields, maxResults=1000)
    existing_issues_num = 0
    new_issues_num = 0
    for issue in issues:
        existing_issue = Issue.query.filter_by(key=issue.key).first()
        if issue.fields.resolutiondate:
            issue_resolutiondate = strftime("%Y-%m-%d", strptime(issue.fields.resolutiondate[0:10], '%Y-%m-%d'))
        else:
            issue_resolutiondate = None
        if existing_issue:
            existing_issue.status = issue.fields.status.name
            if existing_issue.status == '关闭':
                existing_issue.pro_status = ProStatus.query.filter_by(name='已上线').first()
            existing_issue.summary = issue.fields.summary
            existing_issue.resolutiondate = issue_resolutiondate
            existing_issue.updated = strftime("%Y-%m-%d", strptime(issue.fields.updated[0:10], '%Y-%m-%d'))
            db.session.commit()
            existing_issues_num += 1
        else:
            new_issue = Issue(
                key=issue.key,
                jira_id=int(issue.id),
                status=issue.fields.status.name,
                created_time=strftime("%Y-%m-%d", strptime(issue.fields.created[0:10], '%Y-%m-%d')),
                resolutiondate=issue_resolutiondate,
                updated=strftime("%Y-%m-%d", strptime(issue.fields.updated[0:10], '%Y-%m-%d')),
                summary=issue.fields.summary,
                creator=issue.fields.creator.displayName,
                url=str(server + '/browse/' + issue.key)
            )
            db.session.add(new_issue)
            db.session.commit()
            new_issues_num += 1
    last_time.last_request_time = date.today()
    db.session.commit()
    return msg1 + '共查询了 %s 条记录，更新了 %s 条已存在记录，新增 %s 条记录' % (existing_issues_num + new_issues_num, existing_issues_num, new_issues_num)


