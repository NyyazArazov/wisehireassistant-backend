from mongoengine import Document, StringField

class Details(Document):
    name = StringField(required=True)
    rank = StringField(required=True)
    consistency = StringField(required=True)
    position_id = StringField(required=True)
