#!/usr/bin/env python
# encoding: utf-8

import os
import json
import re
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo
from pymongo import MongoClient

# Configure the Flask application to connect with the MongoDB server
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/job_applications"
app.config['MONGO_DBNAME'] = 'Indeed'
#app.config['SECRET_KEY'] = 'secret_key'

# Connect to MongoDB using Flask's PyMongo wrapper
mongo = PyMongo(app)
db = mongo.db
col = mongo.db["Indeed"]
print ("MongoDB Database:", mongo.db)

# Declare an app function that will return some HTML
@app.route("/mongo")
def connect_mongo():
    pass


@app.route('/', methods=['GET', 'POST'])
def home_page():
    key=request.values.get("key")
    key=request.values.get("key")
    refer=request.values.get("refer")
    refer_plus=request.values.get("refer_plus")
    
    if (key=="Title"):
        mydoc = col.find({refer: { "$regex": key} })
    elif (key=="Skills"):
        mydoc = col.find({refer:{ "$all": [key]} })
    elif (key=="Company"):
        mydoc = col.find({refer:key})
    elif (key=="Location"):
        mydoc = col.find({refer:{ "$regex": key} })
    elif (key=="Location" & refer_plus="Skills"):
        mydoc = col.find({refer: { "$in": [key] },
                          refer_plus: { "$regex": key} })
	else:
        mydoc = col.find({refer:key})
    for x in mydoc:
        print(x)     
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def get_results():
    return render_template('offer.html')

""" @app.route('/results')
def get_results(query):
    offer = mongo.db.data.find_one_or_404({"_id": offer_id})
    return render_template('offer.html', title=offer.title, offer=offer)

@app.route('/offer/<int:offer_id>')
def show_offer(offer_id):
    offer = mongo.db.data.find_one_or_404({"_id": offer_id})
    return render_template('offer.html', title=offer.title, offer=offer)
 """

""" class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    user = User(name=record['name'],
                email=record['email'])
    user.save()
    return jsonify(user.to_json())

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'])
    return jsonify(user.to_json())

@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'}) """


if __name__ == "__main__":
    app.run(debug=True)