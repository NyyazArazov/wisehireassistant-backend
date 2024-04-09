from flask import Blueprint, request
from flask import jsonify
from services.details_service import get_all_details
from services.details_service import save_details
details_route = Blueprint('details_route', __name__)

@details_route.route("/api/details/saveDetails", methods=['POST'])
def saveDetails():    
    details_info = request.json
    resume_json = details_info['resume_json']
    position_id = details_info['position_id']
    similarityResponse = details_info['similarityResponse']
    try:
        result = save_details(resume_json, position_id, similarityResponse)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@details_route.route("/api/details/getAllDetails", methods=['GET'])
def getAllDetails():      
    try:
        data = request.json
        position_id = data.get('position_id')  

        result = get_all_details(position_id)

        return result
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500