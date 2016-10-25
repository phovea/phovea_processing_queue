from __future__ import absolute_import
__author__ = 'Samuel Gratzl'

import sys
#
# change search path
sys.path.append('plugins/')

from celery_app import app

if __name__ == '__main__':
  from caleydo_server.config import view
  cc = view('caleydo_processing_queue.celery')
  import shlex
  print cc.argv
  print shlex.split(cc.argv)
  app.start([__file__]+shlex.split(cc.argv))
