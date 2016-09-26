__author__ = 'Holger Stitz'


from flask import Flask, request, abort
from caleydo_server.util import jsonify

from caleydo_processing_queue.celery_app import app as celery_app
from celery.result import AsyncResult

import logging
_log = logging.getLogger(__name__)

app = Flask(__name__)

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
  res = tasks.add.apply_async((x, y))
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
