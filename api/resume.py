from flask import Blueprint, request
from services.resume_service import upload_service

resume_route = Blueprint('resume_route', __name__)


@resume_route.route("/api/resume/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part' #TODO:404

    file = request.files['file']
    return upload_service(file)
