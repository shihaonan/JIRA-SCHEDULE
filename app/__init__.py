from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_bootstrap import Bootstrap
from flask_whooshee import Whooshee
import flask_excel

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
whooshee = Whooshee(app)
flask_excel.init_excel(app)

from app import views,models