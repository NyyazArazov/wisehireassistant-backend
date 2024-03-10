from mongoengine import Document, StringField


class PDFFile(Document):
    filename = StringField(required=True)
