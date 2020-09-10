import pymongo
from pymongo import MongoClient


connection = MongoClient("mongodb://localhost:27017/")

mydb = connection["indeed_db"]
mycol = connection["indeed_job"]

dblist = connection.list_database_names()
if "indeed_db" in dblist:
    print("The database exists.")

collist = connection.list_collection_names()
if "indeed_job" in collist:
    print("The collection exists.")

    
indeed_dict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_many(indeed_dict)

#print list of the _id values of the inserted documents:
print(x.inserted_ids) 