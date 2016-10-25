#!/usr/bin/env bash

(celery -A caleydo_processing_queue.celery_app -l info --logfile=../logs/%n%I.log)

