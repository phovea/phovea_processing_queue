from __future__ import absolute_import
__author__ = 'Samuel Gratzl'

import sys
# change search path
sys.path.append('plugins/')

from phovea_processing_queue.task_definition import app

if __name__ == '__main__':
  from phovea_server.config import view
  cc = view('phovea_processing_queue.celery')
  import shlex
  app.start([__file__]+shlex.split(cc.argv))
