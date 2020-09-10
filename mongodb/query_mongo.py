import pymongo
from pymongo import MongoClient

# connect to database
connection = MongoClient('localhost', 27017)
db = connection.indeed_db

# handle to movies collection
jobcard = db.indeed_job
# find all
items = jobcard.find({})
print(items)
# find_one
item = jobcard.find_one({})
print(item['title'])
