#!/usr/bin/env bash

(cd ./plugins/ && celery -A caleydo_processing_queue.celery_app worker -l info --logfile=../logs/%n%I.log)

