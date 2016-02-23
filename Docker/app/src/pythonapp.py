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
import pythonapp2
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

#APP CONFIGURATIONS, WILL MOVE THIS TO IT'S OWN FILE
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

#MYSQL CONFIG
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'AppDynamics'
app.config['MYSQL_DATABASE_HOST'] = 'pythondemo-mysql'

#REDIS CONFIG
app.config['REDIS_QUEUE_KEY'] = 'AppDynamicsQueue'
app.config['REDIS_HOST'] = 'pythondemo-redis'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0

#MYSQL CONNECTION
mysql = MySQL()
mysql.init_app(app)


#ELASTICSEARCH CONNECTION
es = Elasticsearch([
	{'host': 'pythondemo-elasticsearch'},
])
esIndex = 'elasticsearchcart'
esDocType = 'item'
##Default Host/Port is localhost:9200

#REDIS CONNECTION AND CONFIG
redis = Redis(app)

#MOVE POSTGRES HERE
postgresDatabase = 'AppDynamicsPostgres'
postgresUser = 'test'
postgresPassword = 'test'
postgresHost = 'pythondemo-postgres'
postgresPort = '5432'

#FOR JEFF
#ALL DATABASE CONNECTIONS IN
#ALL EXTERNAL PACKAGES


@app.route("/")
def main():
    req = urllib2.Request('http://BUNDY_APP')
    response = urllib2.urlopen(req)
    return render_template('viewCatalog.html')

#this is the slow query for mysql
def checkAccount():
    conn = mysql.connect()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    randomNum = randint(1,5)
    if now.minute <= 25:
        if randomNum == 2:
            for x in range(1,3000):
                add_values = (x, '_email', '_password')
                add_person = ("INSERT INTO tbl_user (Id, Name, Email) VALUES (%s, %s, %s)")
                cursor.execute(add_person, add_values)
                cursor.execute("SELECT * FROM tbl_user")
        else:
            for x in range(1,750):
                add_values = (x, '_email', '_password')
                add_person = ("INSERT INTO tbl_user (Id, Name, Email) VALUES (%s, %s, %s)")
                cursor.execute(add_person, add_values)
                cursor.execute("SELECT * FROM tbl_user")
    else:
        for x in range(1,500):
            add_values = (x, '_email', '_password')
            add_person = ("INSERT INTO tbl_user (Id, Name, Email) VALUES (%s, %s, %s)")
            cursor.execute(add_person, add_values)
            cursor.execute("SELECT Id, Name, Email FROM tbl_user")


    data = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return True


#MYSQL INSERT, IF IT''S THE FIRST 15 MINUTES OF THE HOUR, 20% OF THE TIME
#IT'S GOING TO BE A SLOW QUERY BECAUSE OF THE SELECT STATEMENT
@app.route("/showSignUp")
def showSignUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tbl_user")
    cursor.execute("CREATE TABLE tbl_user(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Email VARCHAR(20))")
    booleanvalue = checkAccount()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('viewCatalog.html')

#EXIT CALL TO SELF
@app.route('/http')
def http_exit_call():
    url = request.args.get('url')

    if url is None:
        raise MissingArgumentException('required argument "url" is missing')

    lower_url = url.lower()
    if not lower_url.startswith('http://') and not lower_url.startswith('https://'):
        raise MissingArgumentException('required argument "url" must be a URL with protocol, like http://...')

    resp = requests.get(url)

    return render_template_string(
        "<!DOCTYPE html><title>HTTP Exit Call</title><h1>Response from {{url}}</h1><p>Content length {{len}}</p>",
        url=url, len=resp.headers.get('content-length', 'n/a'))

#THIS PART WILL CALL THE POSTGRES DATABASE, LONG INSERT
@app.route('/viewCatalog')
def viewCatalog():
    conn = psycopg2.connect(database=postgresDatabase, user=postgresUser, host=postgresHost, port=postgresPort, password=postgresPassword)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Inventory")
    cursor.execute("DROP TABLE IF EXISTS Clearence")
    cursor.execute("CREATE TABLE Inventory(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Email VARCHAR(20))")
    cursor.execute("CREATE TABLE Clearence(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Email VARCHAR(20))")
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('viewCatalog.html')

#ELASTICSEARCH DATABASE
@app.route('/addToCart')
def addToCart():

    count = 1;
    doc = {
    'user': 'eric.johanson',
    'item': 'computer',
    }
    res = es.index(index=esIndex, doc_type=esDocType, id=count, body=doc)
    es.search(index='elasticsearchcart', doc_type='item')
    es.indices.refresh(index="elasticsearchcart")
    es.delete(index='elasticsearchcart', doc_type='item', id=count)
    return render_template('viewCatalog.html')

#DUMMY API CALL TO AMAZON
@app.route('/checkout')
@httpretty.activate
def checkout():
    return render_template('viewCatalog.html')

#REDIS CACHE
@cache.memoize(timeout=60)
def query_db():
    return render_template('viewCatalog.html')

#CALL TO FUNCTION ABOVE
@app.route('/viewCart')
def viewCartItems():
    return query_db()

@app.route('/viewCart-removeItem')
def removeItem():
    return render_template('viewCatalog.html')

appHost = '0.0.0.0'
appPort = 5000

if __name__ == "__main__":
    app.run(host=appHost, port=appPort, debug=False, threaded=True)
