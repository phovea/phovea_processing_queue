from __future__ import absolute_import


import os
dir_path = os.getcwd()

if 'plugins' in dir_path:
  os.chdir('../') # change directory when running celery from shell

import caleydo_server.config
cc = caleydo_server.config.view('caleydo_processing_queue')

import logging.config
logging.config.dictConfig(cc.logging)
_log = logging.getLogger(__name__)


def _map(p):
  #print 'add processing tasks: ' + p.module
  _log.info('add processing task: %s', p.module)
  return p.module
from caleydo_server import plugin
task_modules = map(_map, plugin.list('processing-task'))

if 'plugins' in dir_path:
  os.chdir(dir_path) # restore directory when running celery from shell


from celery import Celery
app = Celery(
  'caleydo_processing_queue',
  broker=cc.get('celery.broker'),
  backend=cc.get('celery.backend'),
  include=task_modules
)

# Optional configuration, see the application user guide.
app.conf.update(
  CELERY_TASK_RESULT_EXPIRES=cc.getint('celery.expires'),
)

if __name__ == '__main__':
  app.start()
