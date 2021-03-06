from app import db
from datetime import datetime

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    jira_id = db.Column(db.Integer, unique=True, index=True)
    key = db.Column(db.String(20), unique=True,index=True)
    status = db.Column(db.String(30))
    pro_status_id = db.Column(db.Integer, db.ForeignKey('pro_status.id'))
    created_time = db.Column(db.Date)
    summary = db.Column(db.String(256))
    creator = db.Column(db.String(30))
    url = db.Column(db.String(256))
    ui_schedule = db.Column(db.String(66))
    back_schedule = db.Column(db.String(66))
    front_schedule = db.Column(db.String(66))
    test_schedule = db.Column(db.String(66))
    ui_staff = db.Column(db.String(256))
    back_staff = db.Column(db.String(256))
    front_staff = db.Column(db.String(256))
    test_staff = db.Column(db.String(256))
    is_pro = db.Column(db.Integer)
    resolutiondate = db.Column(db.Date)
    updated = db.Column(db.Date)


# class BigIssue(db.Model):
#     __tablename__ = 'big_issues'
#     id = db.Column(db.Integer, primary_key=True, index=True)
#     jira_id = db.Column(db.Integer, unique=True, index=True)
#     key = db.Column(db.String(20), unique=True,index=True)
#     status = db.Column(db.String(30))
#     pro_status_id = db.Column(db.Integer, db.ForeignKey('pro_status.id'))
#     created_time = db.Column(db.Date)
#     summary = db.Column(db.String(256))
#     creator = db.Column(db.String(30))
#     url = db.Column(db.String(256))
#     related_issues = db.relationship('Issue',backref='related_big_issue',lazy='dynamic')
#     ui_schedule = db.Column(db.String(66))
#     back_schedule = db.Column(db.String(66))
#     front_schedule = db.Column(db.String(66))
#     test_schedule = db.Column(db.String(66))
#     ui_staff = db.Column(db.String(256))
#     back_staff = db.Column(db.String(256))
#     front_staff = db.Column(db.String(256))
#     test_staff = db.Column(db.String(256))


class ProStatus(db.Model):
    __tablename__ = 'pro_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    issues = db.relationship('Issue',backref='pro_status',lazy='dynamic')

class LastTime(db.Model):
    __tablename__ = 'last_time'
    id = db.Column(db.Integer, primary_key=True)
    last_request_time = db.Column(db.Date)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)









