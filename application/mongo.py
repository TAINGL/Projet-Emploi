
# https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_RESTAPI_with_Flask.php
import os
import json
import re
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask import jsonify
from flask import request
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Indeed'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/job_applications'

mongo = PyMongo(app)
job = mongo.db.Indeed

@app.route("/search", methods=['GET', 'POST'])    
def search():
    latest_jobs = job.find().limit(10)
    form = SearchForm()
    if form.validate_on_submit():
        query = {"keywords": re.split(r'\W', form.query.data),
                 "city": form.query.city}
        return get_results(query)
    return render_template("index.html", latest_jobs=latest_jobs, form=form)


    #Searching a Task with various references    
    skills=request.values.get("skills")    
    response = job.find({Skills:skills})    
    return render_template('index.html')    

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def get_results():
    return render_template('offer.html')

@app.route('/test', methods=['GET'])
def get_all_results():
  job = mongo.db.Indeed
  output = []
  myquery = { "Title": { "$regex": "data"} }
  for s in job.find(myquery):
    output.append({
                 'Title' : s['Title'],
                 'Company' : s['Company'],
                 'Location' : s['Location'],
                 'Skills' : s['Skills'],
                 'Links' : s['Links']
                 })
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)