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
        position_id = request.args.get('position_id')
        print(position_id)
        result, status_code = get_all_details(position_id)
        print(result)

        return result, status_code
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
