
# https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_RESTAPI_with_Flask.php
import os
import json
import re
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pymongo import PyMongo
import pymongo 
from bson.json_util import dumps

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Indeed'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/job_applications'
app.config["SECRET_KEY"] = '296e3a31e0fe30ddf14efa247e70b56b' # python :> import secrets > secrets.token_hek(16)

mongo = PyMongo(app)
job_collection = mongo.db.Indeed

class SearchForm(FlaskForm):
    query = StringField('What Skills do you have?')
    city = StringField('Where?')
    company = StringField('Which company?')
    submit = SubmitField('Submit')

@app.route("/")
@app.route("/search", methods=['GET', 'POST'])    
def index():
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit():
        keywords = form.query.data if hasattr(form.query, 'data') else ""
        city = form.query.city if hasattr(form.query, 'city') else ""
        company = form.query.company if hasattr(form.query, 'company') else ""
        return redirect(url_for('get_offers', keywords=keywords, city=city, company=company))
    return render_template('index.html', form=form)

@app.route("/result")    
def get_offers():
    job_collection = mongo.db.Indeed

    keywords = request.args.get("keywords")
    city = request.args.get("city")
    company = request.args.get("company")

    myquery = {}
    if city:
        myquery = { "Location": { "$regex": city }}
    elif city and company:
        myquery = {
        "Company" : { "$in": list(company) },
        "Location" : { "$regex": "paris" }
    }
    elif keywords:
        myquery = { "Skills": { "$all": list(keywords)} }
    else:
        job_collection.find({"exp":10})


    results = job_collection.find(myquery)
    return render_template('offer.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)