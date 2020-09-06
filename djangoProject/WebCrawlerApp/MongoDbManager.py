import pymongo

class MongoDbManager:
    _instance=None
    client=pymongo.MongoClient(host='localhost',port=27017)
    database = client['WebCrawlerDB']['WebCralwerCollection']


###### method #####

