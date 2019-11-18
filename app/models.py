from app import db

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(20), unique=True,index=True)
    status = db.Column(db.String(30))
    pro_status_id = db.Column(db.Integer, db.ForeignKey('pro_status.id'))
    created_time = db.Column(db.Date)
    summary = db.Column(db.String(256))
    creator = db.Column(db.String(30))
    url = db.Column(db.String(256))
    ui_schedule = db.Column(db.String(256))
    back_schedule = db.Column(db.String(256))
    front_schedule = db.Column(db.String(256))
    test_schedule = db.Column(db.String(256))


class ProStatus(db.Model):
    __tablename__ = 'pro_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    issues = db.relationship('Issue',backref='pro_status',lazy='dynamic')











