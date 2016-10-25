from __future__ import absolute_import

from caleydo_processing_queue.celery import task, getLogger

_log = getLogger(__name__)

@task
def add(x, y):
  return float(x) + float(y)


@task
def mul(x, y):
  return float(x) * float(y)


@task
def xsum(numbers):
  return sum(numbers)

