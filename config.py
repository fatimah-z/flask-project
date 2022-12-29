import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_HOST = os.environ.get('DB_HOST', "db")
    DB_NAME = os.environ.get('DB_NAME', "")
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_Password')
    DB_PORT = os.environ.get('DB_PORT')

    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb'://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


