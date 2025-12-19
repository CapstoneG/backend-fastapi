from app.repositories.sentence_repository import SentenceRepository
from app.schemas.sentence_response import SentenceResponse

class SentenceService:
    def __init__(self):
        self.repository = SentenceRepository()

    def get_all_sentences(self):
        sentences = self.repository.find_all()
        return [self._to_response(sen) for sen in sentences]
    
    def get_sentences_by_level(self, level: str):
        sentences = self.repository.find_by_level(level=level)
        return [self._to_response(sen) for sen in sentences]
    
    def get_sentence_by_id(self, sentence_id: str):
        sentence = self.repository.find_by_id(sentence_id=sentence_id)
        return self._to_response(sentence)
    
    def get_sentences_by_topic(self, topic: str):
        sentences = self.repository.find_by_topic(topic=topic)
        return [self._to_response(sen) for sen in sentences]
    
    def create_sentence(self, sentence_data: dict):
        return self.repository.save(sentence_data)
    
    def get_topics(self):
        return self.repository.find_topics()
    
    def get_levels(self):
        return self.repository.find_levels()
    
    def get_sets(self):
        return self.repository.find_sets()
    
    def get_sentences_by_topic_and_level(self, topic: str, level: str):
        sentences = self.repository.find_sentences_by_topic_and_level(topic=topic, level=level)
        return [self._to_response(sen) for sen in sentences]
    
    def get_topics_by_level(self, level: str):
        return self.repository.get_topics_by_level(level=level)
    
    def get_levels_by_topic(self, topic: str):
        return self.repository.get_levels_by_topic(topic=topic)
    
    def _to_response(self, sen):
        return SentenceResponse(
            id = sen.get("id"),
            text = sen.get("text"),
            topic = sen.get("topic"),
            level = sen.get("level"),
            audio_url = sen.get("audio_url")
        )