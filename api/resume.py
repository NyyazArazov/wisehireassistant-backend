from flask import Blueprint, request
from services.resume_service import evaluate_service
import json
resume_route = Blueprint('resume_route', __name__)


@resume_route.route("/api/resume/evaluate", methods=['POST'])
def evaluate():
    if 'file' not in request.files:
        return 'No file part' #TODO:404

    file = request.files['file']
    return json.dumps(evaluate_service(file))
