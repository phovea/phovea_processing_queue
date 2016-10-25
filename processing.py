__author__ = 'Holger Stitz'


from flask import Flask, Response
from caleydo_server.util import jsonify

from caleydo_processing_queue.celery_app import app as celery_app, notifier
from celery.result import AsyncResult

import logging
_log = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/stream')
def stream():
  """
  event source like stream for requesting task results
  :return:
  """
  from caleydo_processing_queue.celery_app import notifier
  import json
  def event_stream():
    for msg in notifier.listen():
      _log.debug('task result id=%s name=%s status=%s',msg['task_id'],msg['task_name'],msg['task_status'])
      yield 'data: {}\n\n'.format(json.dumps(msg))
  return Response(event_stream(), mimetype='text/event-stream')


@app.route('/res/<task_id>', methods=['GET'])
def get_result(task_id):
  """
  returns the result of a task with blocking
  :param task_id:
  :return:
  """
  res = AsyncResult(task_id, app=celery_app)
  return jsonify(res.get())

@app.route('/add/<x>/<y>', methods=['GET'])
def add(x, y):
  import tasks
  res = tasks.add.delay(x, y)
  return res.id



def create():
  """
   entry point of this plugin
  """
  return app

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
