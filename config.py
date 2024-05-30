import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
