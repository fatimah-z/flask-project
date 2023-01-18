import os


class Config(object):
    DB_HOST = os.environ.get('DB_HOST', "db")
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT')
    SECRET_KEY = 'd4c4a1b5c0ad4ee398c3249c70dbdee4'
    REFRESH_KEY = 'ead3922f5c2548f1b44cb192e17d7152'
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
