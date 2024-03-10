import os
from mongoengine import Document, connect, StringField
from gridfs import GridFS
from model.resume import PDFFile

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(PDFFile._get_db())


def upload_service(file):
    pdf_file = PDFFile(filename=file.filename)
    pdf_file.save()

    file_id = fs.put(file, filename=pdf_file.id)
    return str(pdf_file.id)


def get_pdf(file_id):
    pdf_file = PDFFile.objects.get(id=file_id)
    file_obj = fs.get(pdf_file.id)
    return file_obj
