from celery import Celery
from config import Config


# def make_celery(app):
#     celery = Celery(app.import_name)
#     celery.conf.update(app.config["CELERY_CONFIG"])
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery

celery = Celery("app",
                config_source= Config,
                broker="redis://redis:6379/0",
                backend="redis://redis:6379/0",
                include=['app.tasks']
                )
