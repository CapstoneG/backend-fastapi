from app.db.mongodb import db

class SentenceRepository:
    def __init__(self):
        self.collection = db['Sentences']

    def find_all(self):
        return list(self.collection.find())
    
    def find_by_level(self, level: str):
        return list(self.collection.find({'level': level.capitalize()}))
    
    def find_by_id(self, sentence_id: str):
        return self.collection.find_one({'id': sentence_id})
    
    def find_by_topic(self, topic: str):
        return list(self.collection.find({'topic': topic.capitalize()}))
    
    def find_sentences_by_topic_and_level(self, topic: str, level: str):
        return list(self.collection.find({'topic': topic.capitalize(), 'level': level.capitalize()}))
    
    def find_topics(self):
        return self.collection.distinct('topic')
    
    def find_levels(self):
        return self.collection.distinct('level')
    
    def find_sets(self):
        return list(self.collection.aggregate([
            {
                "$group": {
                    "_id": {
                        "level": "$level",
                        "topic": "$topic"
                    },
                "count": { 
                        "$sum": 1 
                    }
                }
            }
        ]))
    
    def get_topics_by_level(self, level: str):
        return self.collection.distinct('topic', {'level': level.capitalize()})
    
    def get_levels_by_topic(self, topic: str):
        return self.collection.distinct('level', {'topic': topic.capitalize()})
    
    def save(self, sentence_data: dict):
        result = self.collection.insert_one(sentence_data)
        return str(result.inserted_id)