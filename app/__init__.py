from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_bootstrap import Bootstrap
import flask_excel

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
flask_excel.init_excel(app)

from app import views
from app.models import Issue,ProStatus


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        all_pro_status = ProStatus.query.order_by(ProStatus.id).all()
        all_creator_query = Issue.query.with_entities(Issue.creator).distinct().all()
        all_creator = ()
        for i in all_creator_query:
            all_creator = all_creator + i
        all_jira_status_query = Issue.query.with_entities(Issue.status).distinct().all()
        all_jira_status = ()
        for i in all_jira_status_query:
            all_jira_status = all_jira_status + i

        return dict(all_pro_status=all_pro_status,all_creator=all_creator,all_jira_status=all_jira_status)


register_template_context(app)