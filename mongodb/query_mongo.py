import pymongo
from pymongo import MongoClient

# connect to database
connection = MongoClient('localhost', 27017)
db = connection.indeed_db

# handle to movies collection
jobcard = db.coljob

# find all
myquery_1 = { "Title": { "$regex": "data"} }
myquery_2 = { "Skills": { "$all": ["python", "r" ]} }
myquery_3 = { "Company": "hurryman" }
myquery_4 = { "Location": { "$regex": "paris"} }
myquery_5 = {
    "Company" : { "$in": ["phenix", "edf"] },
    "Location" : { "$regex": "paris" }
}


mydoc = jobcard.find(myquery_5)

for x in mydoc:
    print(x) 

# find_one
#item = jobcard.find_one({})
#print(item['title'])
