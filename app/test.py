from jira import JIRA
from time import strptime,strftime
from app.models import Issue
from app import db
from datetime import date,timedelta

a=[('苗磊',), ('王珅',), ('施浩楠',), ('董晓玲',), ('郝翠霞',), ('宋世杰',), ('沙婷婷',), ('付丽莉',), ('赵海华',), ('张建文',)]
b=()

for i in a:
    b=b+i
print(b)
for u in b:
    print(u)