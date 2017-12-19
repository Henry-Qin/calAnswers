__author__ = 'henryqin'

import pymongo

URIString = 'mongodb://admin:calanswers@calanswers-shard-00-00-czwdo.mongodb.net:27017,calanswers-shard-00-01-czwdo.mongodb.net:27017,calanswers-shard-00-02-czwdo.mongodb.net:27017/test?ssl=true&replicaSet=CalAnswers-shard-0&authSource=admin'
client = pymongo.MongoClient(URIString)
db = client['CalAnswers']
sampleCollection = db['sample']
query = sampleCollection.find()
for doc in query:
    print(doc)
