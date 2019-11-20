import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ISSUES_PER_PAGE = 50
    WHOOSHEE_MIN_STRING_LEN = 2