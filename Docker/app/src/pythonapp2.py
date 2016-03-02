from __future__ import print_function
import logging
import math
import requests
import time
import sys
import psycopg2
import psycopg2.pool
import httpretty
import config
import datetime
import pythonapp
import urllib2

from flask import Flask, render_template, render_template_string, json, request, abort, session, jsonify
from flaskext.mysql import MySQL
from flask.ext.cache import Cache
from werkzeug import generate_password_hash, check_password_hash
from elasticsearch import Elasticsearch, helpers
from rq import Worker, Queue, Connection
from redis import Redis
from random import randint
from socket import *

#WSGI APP
app = Flask(__name__)

#POSTGRES LABELS
postgresDatabase = 'AppDynamicsPostgres'
postgresUser = 'test'
postgresPassword = 'test'
postgresHost = 'pythondemo-postgres'
postgresPort = '5432'

appHost = '0.0.0.0'
appPort = 1080



@app.route("/")
def main():
    conn = psycopg2.connect(database=postgresDatabase, user=postgresUser, host=postgresHost, port=postgresPort, password=postgresPassword)
    conn.close()
    return render_template('index.html')


@app.route("/signUp")
def signUp():
    req = urllib2.Request('http://PYTHON_APP:5000/showSignUp')
    response = urllib2.urlopen(req)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host=appHost, port=appPort, threaded=True, debug=True)
