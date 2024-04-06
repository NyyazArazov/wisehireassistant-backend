from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, FloatField

class Experience(EmbeddedDocument):
    Company = StringField(required=True)
    Location = StringField(required=True)
    Position = StringField(required=True)
    Duration = StringField(required=True)
    Responsibilities = ListField(StringField())
     
class Education(EmbeddedDocument):
    University = StringField(required=True)
    Location = StringField(required=True)
    Degree = StringField(required=True)
    Duration = StringField(required=True)
    GPA = FloatField()

class Skills(EmbeddedDocument):
    Programming_Languages = ListField(StringField())
    Frontend_Technologies = ListField(StringField())
    Backend_Technologies = ListField(StringField())
    Operating_Systems = ListField(StringField())
    Databases = ListField(StringField())
    Other = ListField(StringField())

class DynamicCandidate(Document):
    Name = StringField(required=True)
    Experience = ListField(EmbeddedDocumentField(Experience))
    Education = EmbeddedDocumentField(Education)
    Skills = EmbeddedDocumentField(Skills)
    Languages = ListField(StringField())
    Technology = ListField(StringField())

