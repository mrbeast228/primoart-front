# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os

bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5005')
workers = 1
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
