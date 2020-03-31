#!/home/day-journal/.pyenv/versions/flask_peewee_3.6.4/bin/python

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
