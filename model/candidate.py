from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, FloatField, EmbeddedDocument


class Experience(EmbeddedDocument):
    company = StringField(required=True)
    location = StringField(required=True)
    position = StringField(required=True)
    duration = StringField(required=True)
    responsibilities = ListField(StringField())


class Education(EmbeddedDocument):
    university = StringField(required=True)
    location = StringField(required=True)
    degree = StringField(required=True)
    duration = StringField(required=True)
    GPA = FloatField()


class Skills(EmbeddedDocument):
    skills = ListField(StringField())
    other = ListField(StringField())


class DynamicCandidate(Document):
    name = StringField(required=True)
    experience = ListField(EmbeddedDocumentField(Experience))
    education = EmbeddedDocumentField(Education)
    skills = EmbeddedDocumentField(Skills)
