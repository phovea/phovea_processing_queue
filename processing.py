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
  from caleydo_processing_queue.celery_app import notifier
  def event_stream():
    channel = notifier.subscribe()
    _log.info('subscribe')
    for msg in channel.listen():
      if msg['type'] != 'message':
        continue
      _log.info('msg %s', str(msg['data']))
      yield 'data: {}\n\n'.format(msg['data'])
  return Response(event_stream(), mimetype='text/event-stream')


@app.route('/hello/<name>', methods=['GET'])
def hello_world(name):
  #"Hello " + name
  _log.info("Hello test toll " + name)

  import caleydo_server.config
  c = caleydo_server.config.view('caleydo_processing_queue')
  return "Hello test bla " + name


@app.route('/add/<x>/<y>', methods=['GET'])
def add(x, y):
  import tasks
  res = tasks.add.delay(x, y)
  return "<a href=\"/api/processing/res/" + res.id + "\">" + res.id + "</a>"

@app.route('/res/<task_id>', methods=['GET'])
def get_result(task_id):
  res = AsyncResult(task_id, app=celery_app)
  return jsonify(res.get())


def create():
  """
   entry point of this plugin
  """
  return app


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
