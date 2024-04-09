from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, FloatField, EmbeddedDocument


class Experience(EmbeddedDocument):
    company = StringField(required=True)
    title = StringField(required=True)


class DynamicCandidate(Document):
    name = StringField(required=True)
    experience = ListField(EmbeddedDocumentField(Experience))
    university = StringField()
    degree = StringField()
    skills = ListField(StringField())
