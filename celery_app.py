from __future__ import absolute_import, print_function
import logging
import functools
from celery import Task
import redis

_log = logging.getLogger(__name__)

def _create_celery():
  import sys
  from celery import Celery
  from caleydo_server.plugin import list as list_plugins
  from caleydo_server.config import view as config_view
  #change search path
  sys.path.append('plugins/')

  #set configured registry
  plugins = list_plugins('processing-task')
  cc = config_view('caleydo_processing_queue')

  def _map(p):
    #print 'add processing tasks: ' + p.module
    _log.info('add processing task: %s', p.module)
    return p.module
  task_modules = map(_map, plugins)

  app = Celery(
    cc.get('celery.name'),
    broker=cc.get('celery.broker'),
    backend=cc.get('celery.backend'),
    include=task_modules
  )

  # Optional configuration, see the application user guide.
  app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=cc.getint('celery.expires')
  )
  return app

class TaskNotifier(object):
  """
  utility to encapsulate the notifier behavior using redis pub usb
  """
  def __init__(self):
    from caleydo_server.config import view as config_view
    cc = config_view('caleydo_processing_queue.celery')
    self._db = redis.Redis(host=cc.host, port=cc.port, db=cc.db)
    self._channel_name = 'caleydo_processing_channel'

  def subscribe(self):
    p = self._db.pubsub(ignore_subscribe_messages=True)
    p.subscribe(self._channel_name)
    return p

  def send(self, task_id, task_name, task_status):
    # send a message using redis
    print('send', task_id, task_name, task_status)
    self._db.publish(self._channel_name, '{{ "task_id": "{}", "task_name": "{}", "task_status": "{}" }}'.format(task_id,task_name,task_status))


class BaseTask(Task):
  """
  base class for processing tasks that report automatically when they are done using redis
  """
  abstract = True

  def on_success(self, retval, task_id, args, kwargs):
    notifier.send(task_id, self.name, 'success')

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    notifier.send(task_id, self.name, 'failure')

notifier = TaskNotifier()

app = _create_celery()
task = functools.partial(app.task, base=BaseTask)

# just expose the needed stuff
__all__ = ['task', 'celery_app', 'BaseTask', 'notifier']

if __name__ == '__main__':
  import logging.config
  from caleydo_server.config import view
  cc = view('caleydo_processing_queue')
  logging.config.dictConfig(cc.logging)

  app.worker_main()
