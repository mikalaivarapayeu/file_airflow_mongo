# importing needed libraries
import pymongo
import json
import glob


# Setting up connection to MongoDB container

client = pymongo.MongoClient('mongodb://root:example@mongo:27017/', username='root', password='example')

db = client['app_reviews']

collection = db['tiktok_reviews']


# # Loading data into DB

file_name_list = glob.glob('/opt/out/*.json')
# print(file_name_list[0])

with open(file_name_list[0]) as f:
    file_data = json.load(f)


for i in range(0,len(file_data)):
    doc_to_insert = file_data[str(i)]
    collection.insert_one(doc_to_insert)


client.close()

