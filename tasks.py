from __future__ import absolute_import

from caleydo_processing_queue.celery_app import app as celery_app
from celery.utils.log import get_task_logger

_log = get_task_logger(__name__)

@celery_app.task
def add(x, y):
  return float(x) + float(y)


@celery_app.task
def mul(x, y):
  return float(x) * float(y)


@celery_app.task
def xsum(numbers):
  return sum(numbers)

