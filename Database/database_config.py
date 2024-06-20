from pymongo import MongoClient

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['Urdu_Shayari']

collection_by_type = db['shayari_by_types']
collection_by_topic = db['shayari_by_topics']
collection_of_conversation = db['ai_conversation']