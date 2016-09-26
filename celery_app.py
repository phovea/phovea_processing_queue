from __future__ import absolute_import

import logging
_log = logging.getLogger(__name__)

import os
dir_path = os.getcwd()

if 'plugins' in dir_path:
  os.chdir('../') # change directory when running celery from shell

def _map(p):
  #print 'add processing tasks: ' + p.module
  _log.info('add processing task: ' + p.module)
  return p.module

from caleydo_server import plugin
task_modules = map(_map, plugin.list('processing-task'))

if 'plugins' in dir_path:
  os.chdir(dir_path) # restore directory when running celery from shell

from celery import Celery

app = Celery(
  'caleydo_processing_queue',
  broker='redis://localhost:6379/5',
  backend='redis://localhost:6379/5',
  include=task_modules
)

# Optional configuration, see the application user guide.
app.conf.update(
  CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
  app.start()
