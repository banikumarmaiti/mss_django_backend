import pymysql

from .settings.celery_worker.worker import app as celery_app


pymysql.install_as_MySQLdb()
__all__ = ("celery_app",)
