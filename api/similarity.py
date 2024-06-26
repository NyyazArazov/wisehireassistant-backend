from flask import Blueprint, request
from flask import jsonify
from services.similarity_service import calculate_similarity_score, save_similarity_score
similarity_route = Blueprint('similarity_route', __name__)

@similarity_route.route('/api/similarity/calculateSimilarity', methods=['POST'])
def calculateSimilarity():
    
    data = request.json
    print(data)
    resume_json = data.get('resume_json')
    position_id = data.get('position_id')

    similarity_score, error = calculate_similarity_score(resume_json, position_id)
    
    if error:
        return jsonify({'error': error}), 404
    #save_similarity_score(similarity_score, candidate_id, position_id)
    return jsonify({'similarity_score': similarity_score})