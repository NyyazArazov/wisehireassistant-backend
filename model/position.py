from mongoengine import Document, StringField

class Position(Document):
    companyName = StringField(required=True)
    jobTitle = StringField(required=True)
    salary = StringField(required=True)
    jobDescription = StringField(required=True)
