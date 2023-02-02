import os


class Config(object):
    DB_HOST = os.environ.get('DB_HOST', "db")
    DB_NAME = os.environ.get('DB_NAME','flaskProject')
    DB_USER = os.environ.get('DB_USER','root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD','root')
    DB_PORT = os.environ.get('DB_PORT','3306')
    SECRET_KEY = 'd4c4a1b5c0ad4ee398c3249c70dbdee4'
    REFRESH_KEY = 'ead3922f5c2548f1b44cb192e17d7152'
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:root@db:3306/flaskProject"
    CELERY_IMPORTS = ["app.tasks",]
    broker_url = 'redis://redis:6379/0'
    result_backend = 'redis://redis:6379/0'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
