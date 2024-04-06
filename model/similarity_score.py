from mongoengine import Document, StringField, FloatField

class SimilarityScore(Document):
    candidate_id = StringField(required=True)
    position_id = StringField(required=True)
    similarity_score = FloatField(required=True)