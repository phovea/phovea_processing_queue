###############################################################################
# Caleydo - Visualization for Molecular Biology - http://caleydo.org
# Copyright (c) The Caleydo Team. All rights reserved.
# Licensed under the new BSD license, available at http://caleydo.org/license
###############################################################################
from __future__ import absolute_import
from phovea_processing_queue.task_definition import app


__author__ = 'Samuel Gratzl'

if __name__ == '__main__':
  from phovea_server.config import view
  import shlex

  cc = view('phovea_processing_queue.celery')

  app.start([__file__] + shlex.split(cc.argv))
