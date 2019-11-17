from app import db

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(20))
    status =  db.Column(db.String(30))
    created_time = db.Column(db.Date)
    summary = db.Column(db.String(256))
    creator = db.Column(db.String(30))
    url = db.Column(db.String(256))
    ui_schedule = db.Column(db.String(256))
    back_schedule = db.Column(db.String(256))
    front_schedule = db.Column(db.String(256))
    test_schedule = db.Column(db.String(256))













