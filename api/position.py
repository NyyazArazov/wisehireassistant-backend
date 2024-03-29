from flask import Blueprint, request
from flask import jsonify
from services.position_service import save_position, delete_position, get_all_positions
position_route = Blueprint('position_route', __name__)

@position_route.route("/api/position/postPosition", methods=['POST'])
def postPosition():    
    position_info = request.json    
    try:
        result = save_position(position_info)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@position_route.route("/api/position/deletePosition/<position_id>", methods=['DELETE'])
def deletePosition(position_id):
    try:
        result = delete_position(position_id)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@position_route.route("/api/position/getAllPositions", methods=['GET'])
def getAllPositions():      
    try:
        result = get_all_positions()

        return result
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500