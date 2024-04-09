from flask import Blueprint, request
from services.candidate_service import save_candidate
from services.resume_service import evaluate_service
resume_route = Blueprint('resume_route', __name__)


@resume_route.route("/api/resume/evaluate", methods=['POST'])
def evaluate():
    if 'file' not in request.files:       
        return 'No file part' #TODO:404
    
    file = request.files['file']
    json_file = evaluate_service(file)
    print(json_file)
    save_candidate(json_file)    
    return json_file
