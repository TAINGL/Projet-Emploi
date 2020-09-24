import json
from ast import literal_eval
import collections  # From Python standard library.
import bson
from bson.codec_options import CodecOptions
from pymongo import MongoClient, errors

# default port is 27017
DOMAIN = 'localhost:'
PORT = 27017

# Create a client object instance using the MongoClient() PyMongo method
# use a try-except indentation to catch MongoClient() errors
try:
    # try to instantiate a client instance
    client = MongoClient(
        host = [ str(DOMAIN) + str(PORT) ],
        serverSelectionTimeoutMS = 3000 # 3 second timeout
    )

    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

except errors.ServerSelectionTimeoutError as err:
    # set the client instance to 'None' if exception
    client = None

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)
	
# Get the database and collection names
if client != None:

    # the list_database_names() method returns a list of strings
    database_names = client.list_database_names()
    

    print ("database_names() TYPE:", type(database_names))
    print ("The client's list_database_names() method returned", len(database_names), "database names.")

    if "job_applications" in database_names:
        print("The database exists.")
    else:
        db = client.indeed_db
        print('The database is created.')
    
    collection_names = db.list_collection_names()

    if "Indeed" in collection_names:
        print("The collection exists.")
    else:
        Indeed = db.Indeed
        print('The collection is created.')

json_file = '../data/Indeed_file.json'
with open(json_file) as f:
        file_data = json.load(f)
        print(f)
        print('File is load')

        data = bson.BSON.encode(file_data)
        decoded_doc = bson.BSON.decode(data)
        print(type(decoded_doc))

    # if pymongo < 3.0, use insert()
    #mycol.insert(file_data)
    # if pymongo >= 3.0 use insert_one() for inserting one document
    #mycol.insert_one(file_data)
    # if pymongo >= 3.0 use insert_many() for inserting many documents
    
        result = db.coljob.insert_many(decoded_doc)

    #print list of the _id values of the inserted documents:
        print('Inserted post id %s ' % result.inserted_id)
        #db.coljob.count()    

client.close()
print('mongo is close')