# from jira import JIRA
# from time import strptime,strftime
# from app.models import Issue
# from app import db
# from datetime import date,timedelta

# server='http://10.9.11.254'
# jira = JIRA(server,basic_auth=('shihaonan','haonan1124'))
# need_fields = 'status,created,summary,creator,updated'
# # fields=need_fields
#
# # 获取全部数据
#
# jql = 'project = DSG AND issuetype in (Bug, 财务需求,需求) AND creator in (membersOf(产品组))'
# # issues = jira.search_issues(jql,maxResults=100)
# p = jira.issue('DSG-11307')
# print(dir(p.fields))
# print(p.fields.resolutiondate)
# print(p.fields.updated)