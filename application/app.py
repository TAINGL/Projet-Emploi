import os
import json
import re
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask import jsonify
from flask import request
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo
import pymongo 
from bson.json_util import dumps

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Indeed'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/job_applications'

mongo = PyMongo(app)
job_collection = mongo.db.Indeed

@app.route("/", methods=['POST'])    
def index():
    query = request.json['q']
    sort = request.json['s']

    job_collection = mongo.db.Indeed
    
    if sort == 'asc':
        result = job_collection.find(query)
    else:
        result = job_collection.find(query).sort('index', pymongo.DESCENDING)
    return dumps(result)

if __name__ == '__main__':
    app.run(debug=True)